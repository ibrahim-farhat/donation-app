# # from django.core.mail import send_mail

# from datetime import date, timedelta
# # import pytest
# # from unittest import mock

# from donors.helpers import calculate_days_from_last_donation

# from .factories import DonorFactory

# # @pytest.mark.django_db
# # @mock.patch("django.core.mail.send_mail")
# # def test_send_response_email_accepted(mock_send_mail):
# #     donation = DonationFactory(donor__user__email='ibrahim.tarek.farhat@gmail.com')
# #     donation_email_code = DonationEmailCode.ACCEPTED
# #     send_response_email(donation, donation_email_code)

# #     mock_send_mail.assert_called_once_with(
# #         subject="Your donation process updates",
# #         message=(
# #             "Your donation has been accepted.\n"
# #             "You can donate again after 3 months.\n"
# #             "Take care of yourself."
# #         ),
# #         from_email='noreply@bloodbank.com',
# #         recipient_list=[donation.donor.user.email],
# #         fail_silently=False
# #     )

# # TODO: Complete send_response_email tests

# def test_calculate_days_from_last_donation(db):
#     last_donation_date = date.today() - timedelta(days=10)
#     donor = DonorFactory(last_donation_date=last_donation_date)
#     assert calculate_days_from_last_donation(donor) == timedelta(days=10).days