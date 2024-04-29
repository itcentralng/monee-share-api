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
        "1. Create -> use this command to create an account on MoneeShare.\n"
        "   Requirements -> your NIN number.\n"
        "   example usage -> create 41xxxxxxxx.\n\n"
        "2. Send -> use this command to send money to other MoneeShare users.\n"
        "   Requirements -> the amount and beneficiary (the receiver).\n"
        "   example usage -> send 2000 +23481xxxxxxxx.\n"
        "   Note1 -> a user's account number is thier mobile phone number.\n"
        "   Note2 -> an account will be created automatically for the beneficiary (if they don't have one already).\n\n"
        "3. Util -> use this command to buy electricity units.\n"
        "   Requirements -> the amount, meter number and the state (the meter is located).\n"
        "   example usage -> util 20000 31xxxxxxxx."
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
    CREATE_SUCCESS = "Your account Was created successfully\n" + Responses.HELP
    CREATE_FAIL = "There was a problem creating an account for {phone_number}"


class PinResponses(StrEnum):
    PIN_CONFIRMATION = "You will get a call from us to enter your PIN"
    PIN_INCORRECT = "PIN incorrect. You have {attempts} attempts left."
    PIN_CORRECT = "PIN correct. Your transaction will be processed shortly."


class TransferResponses(StrEnum):
    SEND_CONFIRMATION = "You are sending N{amount} to {beneficiary}."

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


class UtilResponses(StrEnum):
    UTIL_CONFIRM = (
        "You are buying N{amount} unit for\n"
        "Meter Name: {meter_owner}.\n"
        "Meter Number: {meter_number}.\n"
        "You will receive a call from us to enter your pin number"
    )

    UTIL_SUCCESS = "You token is \n" "{token}\n" + AccountResponses.BALANCE
    UTIL_VERIFICATION_FAILED = "We were unable to find find your meter. Check the meter number ({meter_number}) and try again."
