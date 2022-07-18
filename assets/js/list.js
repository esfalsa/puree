---
---

const regions = {{ site.data.detags | jsonify }};
let zip;

document.querySelector("#teams").addEventListener("change", () => {
  const numTeams = parseInt(document.querySelector("#teams").value);
  const teamsContainer = document.querySelector("#teams-container");

  while (teamsContainer.childElementCount < numTeams) {
    teamsContainer.appendChild(
      generateTeam(teamsContainer.childElementCount + 1)
    );
  }

  while (teamsContainer.childElementCount > numTeams) {
    teamsContainer.lastChild.remove();
  }
});

document
  .querySelector("#generate-list-form")
  .addEventListener("submit", (e) => {
    e.preventDefault();

    zip = new JSZip();

    const update = document.querySelector("#update").value;
    const teams = Array.from(
      document.querySelectorAll("[id^='switch-length-']")
    ).map((switchLength, index) => {
      return {
        index: index,
        switchLength: parseInt(switchLength.value),
      };
    });

    let found = [];
    let allRegions = [];

    teams.forEach((team) => {
      let progress = -team.switchLength;
      let teamRegions = [];

      for (const [index, region] of regions.entries()) {
        if (
          parseInt(region[update]) >= progress + team.switchLength &&
          !found.includes(region.Region)
        ) {
          found.push(region.Region);
          teamRegions.push(region);
          allRegions.push({ ...region, Team: team.index + 1, Index: index });
          progress = parseInt(region[update]);
        }
      }

      team.list = generateList(team.index + 1, teamRegions);
    });

    if (teams.length > 1) {
      allRegions.sort((region1, region2) => {
        return region1.Index > region2.Index ? 1 : -1;
      });

      teams.unshift({
        list: generateList("All_Teams", allRegions),
      });
    }

    const listsContainer = document.querySelector("#lists-container");

    listsContainer.replaceChildren(...teams.map((team) => team.list));
    listsContainer.hidden = false;

    zip.generateAsync({ type: "base64" }).then((data) => {
      document.querySelector(
        "#download-all"
      ).href = `data:application/zip;base64,${data}`;
      document.querySelector("#download-all").classList.remove("disabled");
    });
  });

function generateTeam(index) {
  let team = document.querySelector("#team-template").cloneNode(true);
  team.removeAttribute("id");
  team
    .querySelector(".form-label")
    .setAttribute("for", `switch-length-${index}`);
  team.querySelector(".form-label").textContent = `Team ${index}`;
  team.querySelector(".form-control").id = `switch-length-${index}`;

  return team;
}

function generateList(index, regions, open = false) {
  const isTeam = Boolean(parseInt(index));

  let list = document.querySelector("#list-template").cloneNode(true);
  list.removeAttribute("id");

  list.querySelector(".accordion-header").id = `list-header-${index}`;

  let button = list.querySelector(".accordion-button");
  button.textContent = isTeam ? `Team ${index}` : index.replaceAll("_", " ");
  button.setAttribute("data-bs-target", `#list-collapse-${index}`);
  button.setAttribute("aria-controls", `list-collapse-${index}`);

  list.querySelector(
    ".accordion-collapse.collapse"
  ).id = `list-collapse-${index}`;
  list
    .querySelector(".accordion-collapse.collapse")
    .setAttribute("aria-labelledby", `list-header-${index}`);

  let csv =
    (isTeam ? "" : "Team,") +
    "Region,Issues,Minor,MinorTimestamp,Major,MajorTimestamp\n" +
    regions
      .map(
        (region) =>
          (isTeam ? "" : `${region.Team},`) +
          `"${region.Region}","${region.Issues}",${region.Minor},"${region.MinorTimestamp}",${region.Major},"${region.MajorTimestamp}"`
      )
      .join("\n");

  let downloadButton = list.querySelector("a[download]");
  let fileName = isTeam ? `team${index}.csv` : `${index.toLowerCase()}.csv`;

  downloadButton.download = fileName;
  downloadButton.href = `data:text/csv,${encodeURIComponent(csv)}`;

  zip.file(fileName, csv);

  downloadButton.after(generateTable(regions));

  if (open) {
    button.classList.remove("collapsed");
    list.querySelector(".accordion-collapse").classList.add("show");
  }

  return list;
}

function generateTable(regions) {
  const includeTeamNumbers = Boolean(regions[0].Team);

  let table = document.querySelector("#table-template").cloneNode(true);
  table.removeAttribute("id");

  if (includeTeamNumbers) {
    table.querySelector("thead tr th[team]").removeAttribute("team");
  } else {
    table.querySelector("thead tr th[team]").remove();
  }

  let regionRows = [];

  for (const region of regions) {
    let regionRow = document.querySelector("#tr-template").cloneNode(true);
    regionRow.removeAttribute("id");

    let link = regionRow.querySelector("a");
    link.href = `//www.nationstates.net/region=${region.Region}`;
    link.textContent = region.Region;

    regionRow.children[1].textContent = region.Issues;

    if (includeTeamNumbers) {
      let teamNumber = document.createElement("td");
      teamNumber.textContent = region.Team;
      regionRow.children[0].before(teamNumber);
    }

    regionRow.querySelector("td[minor]").setAttribute("minor", region.Minor);
    regionRow.querySelector(
      "td[minor]"
    ).textContent = `+${region.MinorTimestamp}`;

    regionRow.querySelector("td[major]").setAttribute("major", region.Major);
    regionRow.querySelector(
      "td[major]"
    ).textContent = `+${region.MajorTimestamp}`;

    regionRows.push(regionRow);
  }

  table.querySelector("tbody").replaceChildren(...regionRows);

  return table;
}
