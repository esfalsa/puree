import xml.etree.ElementTree as ElementTree

tree = ElementTree.parse("regions.xml")
root = tree.getroot()

regions = []


def find_issues(region):
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
    ):
        issues = []

    return issues


for region in root.findall("REGION"):
    issues = find_issues(region)
    if len(issues) > 0:
        name = region.find("NAME").text
        regions.append(
            f"<li><a href='//www.nationstates.net/region={name}' target='_blank'>{name}</a> ({', '.join(issues)})</li>\n"
        )

with open("_includes/detags.html", "w") as outfile:
    outfile.writelines(regions)
