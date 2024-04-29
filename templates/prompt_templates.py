format_user_text_template = (
    "Answer the user query.\n"
    "{format_instructions}\n"
    "{user_query}\n"
    "The user query may be in a local Nigerian language.\n"
    "Translate if necessary.\n"
    "The user can request:\n"
    "- Check account balance (e.g., 'balance').\n"
    "- Transfer money to other users/accounts (e.g., 'send [amount] [beneficiary_phone_number]').\n"
    "- Request assistance or instructions.\n"
    "- Pay utility bills (e.g., 'util [amount] [meter number]').\n"
    "- Create an account (e.g., 'create [national_identity_number]').\n"
)
