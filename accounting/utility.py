from django.core.mail import send_mail

def send_signup_confirmation_email(user_email):
    subject = 'Signup Confirmation'
    message = 'Thank you for signing up. Your account has been successfully created.'
    from_email = 'your_email@example.com'  # Replace with your email address or a placeholder
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)
