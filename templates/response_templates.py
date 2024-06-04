from enum import StrEnum
from dotenv import load_dotenv
import os

load_dotenv()
MONEESHARE_SHORTCODE = os.environ.get("AFRICASTALKING_SENDER")


class Responses(StrEnum):
    HELP = (
        "Welcome to Monee Share.\n"
        "Your Text-based banking companion.\n"
        f"Send your commands to {MONEESHARE_SHORTCODE}.\n"
        "Below are a few commands to start with.\n\n"
        "1. Create -> use this command to create an account on Monee Share.\n"
        "   Requirements -> your NIN number.\n"
        "   example usage -> create 41xxxxxxxx.\n\n"
        "2. Send -> use this command to send money to other Monee Share users.\n"
        "   Requirements -> the amount and beneficiary (the receiver).\n"
        "   example usage -> send 2000 +23481xxxxxxxx.\n"
        "   Note1 -> a user's account number is their mobile phone number.\n"
        "   Note2 -> an account will be created automatically for the beneficiary (if they don't have one already).\n\n"
        "3. Util -> use this command to buy electricity units.\n"
        "   Requirements -> the amount, meter number and the state (the meter is located).\n"
        "   example usage -> util 20000 31xxxxxxxx."
    )
    HELP_SHORT = (
        "Below are a few commands to start with.\n\n"
        "1. Create -> create NIN\n"
        "2. Send -> send amount phone_number\n"
        "3. Util -> util amount meter_number state"
    )


class FormatResponses(StrEnum):
    NOT_UNDERSTOOD = "Your command was not understood. Please try again or send 'help', to see all commands."

    BAD_FORMAT = (
        "Your command was not formated correctly. Send 'help' for more information"
    )

    NO_COMMAND_FOUND = (
        "No command found. Please try again or send 'help', to see all commands."
    )


class AccountResponses(StrEnum):
    BALANCE = "Your balance is {balance}."
    CREATE_SUCCESS = "Your account Was created successfully\n" + Responses.HELP_SHORT
    CREATE_FAIL = "There was a problem creating an account for {phone_number}"


class PinResponses(StrEnum):
    PIN_CONFIRMATION = "You will get a call from us to enter your PIN"
    PIN_INCORRECT = "PIN incorrect. You have {attempts} attempts left."
    PIN_CORRECT = "PIN correct. Your transaction will be processed shortly."


class TransferResponses(StrEnum):
    SEND_CONFIRMATION = "You are sending N{amount} to {beneficiary}. You will get a call to confirm this transaction"

    SEND_EXISTS_SENDER = (
        "You have successfully sent N{amount} to {beneficiary}.\n"
        + AccountResponses.BALANCE
    )
    SEND_EXISTS_RECEIVER = (
        "You have recieved N{amount} from {sender}.\n" + AccountResponses.BALANCE
    )

    SEND_NOT_EXIST_SENDER = (
        "An account was created for {beneficiary}.\n"
        "Your have successfully sent N{amount} to {beneficiary}.\n"
        + AccountResponses.BALANCE
    )
    SEND_NOT_EXIST_RECEIVER = Responses.HELP + "\n" + SEND_EXISTS_RECEIVER
    INSUFFICIENT_FUNDS = "Insufficient funds. Fund account and try again"


class UtilResponses(StrEnum):
    UTIL_CONFIRM = (
        "You are buying N{amount} unit for\n"
        "Meter Name: {meter_owner}.\n"
        "Meter Number: {meter_number}.\n\n"
        "You will receive a call from us to enter your pin number"
    )

    UTIL_PURCHASE_SUCCESS = (
        "You token is \n{token}\n" + AccountResponses.BALANCE + "\nAmount: {amount}"
    )
    UTIL_VERIFICATION_FAILED = "We were unable to find your meter. Check the meter number ({meter_number}) and try again."
    UTIL_PURCHASE_FAILED = "Failed to buy utility package. Please try again."
