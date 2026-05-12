import msal


def build_msal_app(client_id: str, client_secret: str, tenant_id: str):
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    return msal.ConfidentialClientApplication(
        client_id, authority=authority, client_credential=client_secret
    )
