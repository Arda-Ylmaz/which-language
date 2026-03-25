# frozen_string_literal: true

require_relative 'base_codex'
require 'net/http'
require 'json'
require 'uri'
require 'time'
require 'fileutils'
require 'openssl'

# GroqCodex: Adapter for high-performance inference via Groq API.
# Metadata and detailed descriptions are handled via config/codexes.yml.
class GroqCodex < BaseCodex
  # Groq API endpoint for chat completions
  def initialize(config = {})
    super('groq', config) # Shared configs are handled by BaseCodex
    @api_key = config[:api_key] || ENV['GROQ_API_KEY']
    @api_url = config[:api_url]

    # Model name and cooldown configuration fetched from config/codexes.yml
    @model_name = config[:model] || config[:model_name]
    @cooldown_seconds = config[:cooldown_seconds] || 1.5

    # Pricing metrics loaded dynamically from external configuration
    @price_input_1m = config[:price_input_1m] || 0.0
    @price_output_1m = config[:price_output_1m] || 0.0

    # Ensure essential configuration is present before proceeding
    raise CodexError, 'GROQ_API_KEY not configured' unless @api_key
    raise CodexError, 'API URL not configured for Groq' unless @api_url
    raise CodexError, 'Model name not configured for Groq' unless @model_name
  end

  def version
    @model_name
  end

  # Performs a lightweight request to verify API connectivity and model readiness
  def warmup(warmup_dir)
    puts "  Warmup: Running trivial prompt on Groq (#{@model_name})..."
    result = run_generation('Respond with just OK.', dir: warmup_dir)
    puts "  Warmup done in #{result[:elapsed_seconds]}s (success=#{result[:success]})"
    sleep(@cooldown_seconds)
    result
  end

  # Main generation loop: Calls API, calculates costs, logs metadata, and saves files
  def run_generation(prompt, dir:, log_path: nil)
    start_time = Time.now

    begin
      response_text, input_tokens, output_tokens = call_groq_api(prompt)
      cost_usd = calculate_cost(input_tokens, output_tokens)
      elapsed = Time.now - start_time

      # Persistent logging for audit trails and performance analysis
      if log_path
        FileUtils.mkdir_p(File.dirname(log_path))
        log_data = {
          model: @model_name,
          prompt: prompt,
          response: response_text,
          input_tokens: input_tokens,
          output_tokens: output_tokens,
          cost_usd: cost_usd,
          elapsed_seconds: elapsed.round(1)
        }
        File.write(log_path, JSON.pretty_generate(log_data))
      end

      # Post-processing: Extract and store the generated source code (Delegated to BaseCodex)
      save_generated_code(response_text, dir)
      sleep(@cooldown_seconds) # Respect rate limits

      {
        success: true,
        elapsed_seconds: elapsed.round(1),
        metrics: {
          input_tokens: input_tokens,
          output_tokens: output_tokens,
          cost_usd: cost_usd,
          model: @model_name,
          duration_ms: (elapsed * 1000).round
        },
        response_text: response_text
      }
    rescue StandardError => e
      puts "!!! GROQ DEBUG ERROR: #{e.message}"
      elapsed = Time.now - start_time
      {
        success: false,
        elapsed_seconds: elapsed.round(1),
        metrics: nil,
        error: "Groq Error: #{e.message}"
      }
    end
  end

  private

  # Executes the HTTP POST request to the Groq backend
  def call_groq_api(prompt)
    uri = URI.parse(@api_url) # Use the instance variable instead of a constant
    
    system_instruction = <<~TEXT
      You are a senior software engineer. 
      Respond ONLY with the source code. 
      Do not include any conversational text, explanations, or notes.
      Always wrap your code in triple backticks with the correct language identifier.
    TEXT

    request_body = {
      model: @model_name,
      messages: [
        { role: 'system', content: system_instruction },
        { role: 'user', content: prompt }
      ],
      temperature: 0.1,
      max_tokens: 4096 
    }

    http = Net::HTTP.new(uri.host, uri.port)
    http.use_ssl = true
    http.read_timeout = 60

    request = Net::HTTP::Post.new(uri.path)
    request['Content-Type'] = 'application/json'
    request['Authorization'] = "Bearer #{@api_key}"
    request.body = JSON.generate(request_body)

    response = http.request(request)

    unless response.is_a?(Net::HTTPSuccess)
      error_msg = JSON.parse(response.body)['error']['message'] rescue response.body
      raise CodexError, "Groq API error (#{response.code}): #{error_msg}"
    end

    data = JSON.parse(response.body)
    response_text = data.dig('choices', 0, 'message', 'content') || ''
    usage = data['usage'] || {}
    
    [response_text, usage['prompt_tokens'] || 0, usage['completion_tokens'] || 0]
  end

  # Cost calculation based on per-million token pricing from config
  def calculate_cost(input_tokens, output_tokens)
    input_cost = (input_tokens / 1_000_000.0) * @price_input_1m
    output_cost = (output_tokens / 1_000_000.0) * @price_output_1m
    (input_cost + output_cost).round(8)
  end
end
