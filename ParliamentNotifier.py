import requests
import pync
import time

# Options
ignore_do_not_disturb = True

notified_vote = -1
notified_speech = {}

# Change session if the house changes session
parameters = {
    "session" : "43-2",
    "format" : "json",
}

# Politicians you want to be notified about
politicians = [
    "justin-trudeau",
    "erin-otoole",
    "jagmeet-singh",
    "elizabeth-may"
]

first_pass = True

for politician in politicians:
    notified_speech[politician] = ""

while True:
    # Handle the data when a new bill is voted on / passed into law
    response = requests.get("https://api.openparliament.ca/votes", params=parameters)
    reset = False
    for response_data in response.json()["objects"]:
        if response_data["number"] != notified_vote:
            reset = True
            pync.notify(
                response_data["description"]["en"], 
                title="Bill #" + str(response_data["number"]),
                subtitle=response_data["result"] + " with " + str(response_data["yea_total"]) + " yes's and " + str(response_data["nay_total"]) + " no's",
                open="https://openparliament.ca/" + response_data["url"],
                appIcon="https://pbs.twimg.com/profile_images/862438537446256640/LR2CNyri_400x400.jpg",
                ignoreDnD=ignore_do_not_disturb
                )
            if first_pass:
                break
        else:
            break
    if reset:
        notified_vote = response.json()["objects"][0]["number"]

    # Handle the data when a MP is speaking
    for politician in politicians:
        parameters_2 = {"politician" : politician, "format" : "json"}
        response_2 = requests.get("https://api.openparliament.ca/speeches", params=parameters_2)
        reset = False
        for response_data_2 in response_2.json()["objects"]:
            if response_data_2["url"] != notified_speech[politician]:
                reset = True
                try:
                    pync.notify(
                        politician.replace('-', ' ').title() +  " spoke on " + response_data_2["h2"]["en"] + " during the " + str(response_data_2["h1"]["en"]),
                        title=politician.replace('-', ' ').title() + " Spoke",
                        open="https://openparliament.ca/" + response_data_2["url"],
                        appIcon="https://pbs.twimg.com/profile_images/862438537446256640/LR2CNyri_400x400.jpg",
                        contentImage="https://api.openparliament.ca/media/polpics/{0}.jpg".format(politician),
                        ignoreDnD=ignore_do_not_disturb
                    )
                except:
                    try:
                        pync.notify(
                            "",
                            title=politician.replace('-', ' ').title() + " Spoke",
                            open="https://openparliament.ca/" + response_data_2["url"],
                            appIcon="https://pbs.twimg.com/profile_images/862438537446256640/LR2CNyri_400x400.jpg",
                            contentImage="https://api.openparliament.ca/media/polpics/{0}.jpg".format(politician),
                            ignoreDnD=ignore_do_not_disturb
                        )
                    except:
                        pass
                if first_pass:
                    break
            else:
                break
        if reset:
            notified_speech[politician] = response_2.json()["objects"][0]["url"]
    if first_pass:
        first_pass = False
    time.sleep(10800)
