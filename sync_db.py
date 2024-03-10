import time
import os
from dotenv import load_dotenv
from convex import ConvexClient
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from utils.haven import SafeHaven

router = APIRouter()
haven = SafeHaven()


CONVEX_URL = os.environ.get("CONVEX_URL")

convex_client = ConvexClient(os.environ.get("CONVEX_URL"))


class User(BaseModel):
    safehavenId: str
    firstName: str
    lastName: str
    phone: str
    account: str
    nin: str
    bvn: str


async def sync_users():
    count = 0
    users = await haven.get_accounts()
    if "data" in users:
        for user in users["data"]:
            payload = {
                "safehavenId": user["_id"],
                "firstName": user["subAccountDetails"]["firstName"],
                "lastName": user["subAccountDetails"]["lastName"],
                "phone": user["subAccountDetails"]["phoneNumber"],
                "account": user["accountNumber"],
                "email": user["subAccountDetails"]["emailAddress"],
                "bvn": user["subAccountDetails"]["bvn"],
                # "nin": user["subAccountDetails"]["nin"] or "",
                "nin": "",
            }
            convex_client.mutation(
                "users:insert",
                jsonable_encoder(payload),
            )
            count += 1
            time.sleep(0.5)
        print(f"Added {count} users")
    print(users)
    return users


async def sync_services():
    count = 0
    services = await haven.get_services()
    if "data" in services:
        for service in services["data"]:
            payload = {
                "safehavenId": service["_id"],
                "name": service["name"],
                "identifier": service["identifier"],
                "description": service["description"],
            }
            convex_client.mutation(
                "services:insert",
                jsonable_encoder(payload),
            )
            count += 1
            time.sleep(0.5)
        print(f"Added {count} services")

    print(services)
    return services


async def sync_categories():
    count = 0
    services = convex_client.query(
        "services:get",
    )

    if not len(services):
        print(services)
        return services

    else:
        for service in services:
            categories = await haven.get_categories(service["safehavenId"])

            if "data" not in categories:
                print(categories)
                return categories
            else:
                for category in categories["data"]:
                    payload = {
                        "serviceId": service["_id"],
                        "safehavenId": category["_id"],
                        "name": category["name"],
                        "identifier": category["identifier"],
                        "description": category["description"],
                    }
                    convex_client.mutation(
                        "categories:insert",
                        jsonable_encoder(payload),
                    )
                    count += 1
                    time.sleep(0.5)
            print(f"Added {count} categories")


@router.get("/")
async def sync():
    # await sync_users()
    # await sync_services()
    # await sync_categories()
    return {"status": 200, "message": "successfully synced"}
