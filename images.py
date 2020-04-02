from random import randint
import aiohttp
import credentials

cache = {};

async def load():
    async with aiohttp.ClientSession() as session:
        fetching = [ no_image ];
        for x in range(len(roll_images)):
            for y in range(len(roll_images[x])):
                fetching.append(roll_images[x][y])

        for x in range(len(crit_success_images)):
            fetching.append(crit_success_images[x])
        for x in range(len(crit_fail_images)):
            fetching.append(crit_fail_images[x])

        while len(fetching) > 0:
            async with session.get('https://api.tenor.com/v1/gifs?media_filter=minimal&key=' + credentials.tenor_key + "&ids=" + ",".join(str(x) for x in fetching[:20])) as resp:
                json = await resp.json()
                results = json["results"]
                for x in range(len(results)):
                    result = results[x]
                    cache[str(result["id"])] = result["media"][0]["gif"]["url"]
                    fetching.remove(int(result["id"]))
def tenor(link):
    return cache[str(link)]



roll_images_index = -1;
roll_images = [
    [ 7859548, 11012957, 4422582, 4522329 ],
    [ 7399305, 10423165, 5133091, 9733935 ],
    [ 5436796, 4802586, 12739180, 4780258 ],
    [ 9503067, 5110385, 12368771, 10891885 ],
    [ 15097387, 14509624, 5188601, 15051103 ],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
]
crit_success_images = [ 16375121, 8055825, 5928196, 13780914 ]
crit_fail_images = [ 14888492, 10893043, 12137800, 8899533 ]

no_image = 5012690

def roll(roll):
    if len(roll_images) <= roll:
        return tenor(no_image)

    if len(roll_images[roll + roll_images_index]) == 0:
        return tenor(no_image)

    return tenor(roll_images[roll + roll_images_index][randint(0, len(roll_images[roll + roll_images_index]) - 1)])

def crit_success():
    return tenor(crit_success_images[randint(0, len(crit_success_images) - 1)])

def crit_fail():
    return tenor(crit_fail_images[randint(0, len(crit_fail_images)) - 1])
