from datetime import timedelta, datetime
import xml.etree.ElementTree as ElementTree

passworded = (
    ElementTree.parse("passworded.xml").getroot().find("REGIONS").text.split(",")
)

tree = ElementTree.parse("regions.xml")
root = tree.getroot()

regions = []

update_start = int(root.find("REGION").find("LASTUPDATE").text)
update_length = int(root.find("REGION[last()]").find("LASTUPDATE").text) - update_start


def find_issues(region):
    if (
        region.find("NAME").text
        in [
            "Suspicious",
            "The Black Hawks",
            "The Brotherhood of Malice",
            "Lily",
            "Osiris",
        ]
        or "X" not in region.find("DELEGATEAUTH").text
        or region.findall("./EMBASSIES/EMBASSY[.='Antifa']")
        or region.find("DELEGATE").text != "0"
    ):
        return []

    issues = []

    if (wfe := region.find("FACTBOOK").text) is not None and any(
        substring in wfe.lower()
        for substring in [
            "[region]the brotherhood of malice[/region]",
            "[region]the black hawks[/region]",
            "[region]valle de arena[/region]",
            "[region]lily[/region]",
            "region=the_brotherhood_of_malice",
            "region=the_black_hawks",
            "region=valle_de_arena",
            "region=lily",
        ]
    ):
        issues.append("WFE")

    if any(
        officer.find("OFFICE").text
        in ["Raider Unity", "Thorn1000", "JOIN TBH", "Join %%Lily%%", "Lily"]
        for officer in region.find("OFFICERS").findall("OFFICER")
    ):
        issues.append("RO")

    if any(
        region.findall(f"./EMBASSIES/EMBASSY[.='{substring}']")
        for substring in [
            "The Black Hawks",
            "The Brotherhood of Malice",
            "Valle de Arena",
            "Red Front",
            "Plum Island",
        ]
        if region.find(f"./EMBASSIES/EMBASSY[.='{substring}']") is not None
        and region.find(f"./EMBASSIES/EMBASSY[.='{substring}']").get("type")
        not in ["closing", "rejected"]
    ):
        issues.append("Embassies")

    return issues


for region in root.findall("REGION"):
    if region.find("NAME").text in passworded:
        continue
    issues = find_issues(region)
    if len(issues) > 0:
        name = region.find("NAME").text
        progress = (int(region.find("LASTUPDATE").text) - update_start) / update_length
        minor_progress = round(progress * 3600)
        major_progress = round(progress * 5400)

        regions.append(
            {
                "region": f'"{name}"',
                "issues": f"\"{', '.join(issues)}\"",
                "minor": str(minor_progress),
                "minor_timestamp": f'"{str(timedelta(seconds=minor_progress))}"',
                "major": str(major_progress),
                "major_timestamp": f'"{str(timedelta(seconds=major_progress))}"',
            }
        )

with open("_data/detags.csv", "w") as outfile:
    outfile.writelines(
        ["Region,Issues,Minor,MinorTimestamp,Major,MajorTimestamp\n"]
        + [(",".join(list(region.values())) + "\n") for region in regions]
    )

with open("_includes/count.html", "w") as outfile:
    outfile.write(str(len(regions)))

with open("_data/history.csv", "a") as outfile:
    outfile.write(
        f"{(datetime.utcfromtimestamp(update_start) - timedelta(1)).strftime('%d %B %Y')},{str(len(regions))}\n"
    )
