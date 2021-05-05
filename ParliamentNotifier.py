import requests
import pync
import time

notified_vote = -1
notified_speech = {}
ignore_do_not_disturb = True

parameters = {
    "session" : "43-2",
    "format" : "json",
}

politicians = [
    "justin-trudeau",
    "erin-otoole",
    "jagmeet-singh",
    "elizabeth-may"
]

for politician in politicians:
    notified_speech[politician] = ""

while True:
    # Handle the data when a new bill is voted on / passed into law
    response = requests.get("https://api.openparliament.ca/votes", params=parameters)
    response_data = response.json()["objects"][0]
    if response_data["number"] != notified_vote:
        notified_vote = response_data["number"]
        pync.notify(
            response_data["description"]["en"], 
            title="Bill #" + str(response_data["number"]),
            subtitle=response_data["result"] + " with " + str(response_data["yea_total"]) + " yes's and " + str(response_data["nay_total"]) + " no's",
            open="https://openparliament.ca/" + response_data["url"],
            appIcon="https://pbs.twimg.com/profile_images/862438537446256640/LR2CNyri_400x400.jpg",
            ignoreDnD=ignore_do_not_disturb
            )

    # Handle the data when a speaker is speaking
    for politician in politicians:
        parameters_2 = {"politician" : politician, "format" : "json"}
        response_2 = requests.get("https://api.openparliament.ca/speeches", params=parameters_2)
        response_data_2 = response_2.json()["objects"][0]
        if response_data_2["url"] != notified_speech[politician]:
            notified_speech[politician] = response_data_2["url"]
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
    time.sleep(1800)
