import xml.etree.ElementTree as ElementTree

tree = ElementTree.parse("regions.xml")
root = tree.getroot()

regions = []

update_start = int(root.find("REGION").find("LASTUPDATE").text)
update_length = int(root.find("REGION[last()]").find("LASTUPDATE").text) - update_start


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
        progress = (int(region.find("LASTUPDATE").text) - update_start) / update_length
        minor_progress = progress * 3600
        major_progress = progress * 5400

        regions.append(
            f"<tr>\n  <td><a href='//www.nationstates.net/region={name}' target='_blank'>{name}</a></td>\n  <td>{', '.join(issues)}</td>\n  <td>+{int(minor_progress // 60)}:{round(minor_progress % 60):02d}</td>\n  <td>+{int(major_progress // 60)}:{round(major_progress % 60):02d}</td>\n</tr>\n"
        )

with open("_includes/detags.html", "w") as outfile:
    outfile.writelines(regions)
