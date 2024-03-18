import secrets

def generate_otp(length=6):
  """Generates a random, time-based OTP of the specified length (default 6 digits).

  Args:
      length: The desired length of the OTP (default 6).

  Returns:
      A string containing the generated OTP.
  """
  random_bytes = secrets.token_bytes(length)
  otp = ''.join(str(b % 10) for b in random_bytes)
  return otp