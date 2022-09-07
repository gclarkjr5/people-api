from fastapi import FastAPI, HTTPException
import redis


r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

app = FastAPI()


@app.get("/names/{person}")
async def get_one_name(person):
    person_exists = r.sismember(name="names", value=f"{person}")

    if not person_exists:
        raise HTTPException(status_code=404, detail=f'{person} does not exist in "names".')

    received_people = r.smembers(name="names")

    received_person = {"name": None}

    for p in received_people:
        if p == person:
            received_person["name"] = p
            break

    return received_person


@app.post("/names/{name}", status_code=201)
async def insert_wesley(name):
    number_added = r.sadd("names", f"{name}")

    if number_added == 0:
        return f'{name} already exists in the set "names"'

    return f"{name} was successfully added"


@app.get("/names")
async def get_names():
    names = r.smembers("names")

    if not names:
        return f'No one has been added to "names" yet.'

    return names


@app.delete("/names/{name}")
async def delete_one_name(name):
    deleted = r.srem("names", f"{name}")

    if deleted == 0:
        return f'{name} does not exist in "names".'

    return f"successfully removed {name}"


@app.delete("/names")
async def clear_all_names():
    members = r.smembers("names")

    mems = []
    for member in members:
        r.srem("names", f"{member}")
        mems.append(member)

    return f"Successfully removed {', '.join(mems)}"
