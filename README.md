# Purée

[Purée](https://esfalsa.github.io/puree) is an easy-to-use website that flags NationStates regions which may have been tagged.

## Features

Purée allows you to…

- Identify regions that may have been tagged
- Track the number of regions found over time
- Generate lists of regions to detag

## Flagging Criteria

For each vulnerable region, Purée scans the World Factbook Entry, open and requested embassies, names of Regional Officer positions, and names of nations who appointed current Regional Officers.

<details>
<summary>

#### World Factbook Entry

</summary>

The World Factbook Entry is flagged if it contains links to…

- the Brotherhood of Malice [region](https://www.nationstates.net/region=the_brotherhood_of_malice)
- the Black Hawks [region](https://www.nationstates.net/region=the_black_hawks) or [forums](https://www.forum.the-black-hawks.org/)
- the Valle de Arena [region](https://www.nationstates.net/region=valle_de_arena)
- the Lily [region](https://www.nationstates.net/region=lily) or [forums](https://lilystates.proboards.com/)
- the Lone Wolves United [region](https://www.nationstates.net/region=lone_wolves_united)
- the Europeian [Office of Naval Recruitment](https://forums.europeians.com/index.php?forums/office-of-naval-recruitment.59364)
- the East Pacific [Executive Application Thread](https://forum.theeastpacific.com/executive-application-thread-t16445.html)
- the West Pacific [_How To War in NationStates_ dispatch](https://www.nationstates.net/page=dispatch/id=1344417)
</details>
<details>
<summary>

#### Embassies

</summary>

Embassies are flagged if they are open or requested (not closing or rejected) and are with…

- The Black Hawks
- The Brotherhood of Malice
- Valle de Arena
- Red Front
- Plum Island
- Kingdom of Australia
- Pasridi Confederacy
</details>
<details>
<summary>

#### Regional Officers

</summary>

Regional officers are flagged if their position is named…

- Raider Unity
- Thorn1000
- Join TBH
- Join %%Lily%%
- Lily
- The Funny
- Empress Wasc
- ERN
- TWPirate
- TWPirates
- Kanye Omari West
- Aga Gang
- EPSA
- Hellfire Hawk

Regional officers are also flagged if they were appointed by a nation matching any of the [regular expressions](https://en.wikipedia.org/wiki/Regular_expression)…

- `guy_\d+`
- `rc_cola_\d+`
- `ijaka(\d|10)`
- `taiko_no_tatsujin_\d+`
- `bobberino\d+`
- `\d+(rd|th|nd|st)_catgirl_division`
- `switz_got_lazy_\d+`
- `switz_\d+`
- `sweeze_\d+`
- `tls_\d+`
- `flap_flap_boom_\d+`
- `liliarchy_ancillary_\d+`
- `lucklife_\d+`
- `lurklife_\d+`
- `wednesday_\d+`
- `thursday_\d+`
- `thorn\d+`
- `wascoitan_?\d+`
- `pineappe_on_pizza_is_good_\d+`
- `foxes_\d+`
- `oversized_operativez_\d+`
- `cretanja_garrison_\d+`
- `legionnaries_{roman_numeral_regex}`
- `legionnary_{roman_numeral_regex}`
- `souls\d+`
- `rb\d+`
- `remus_\d+`
- `remus_{roman_numeral_regex}`
- `yor_\d+`
- `punch_from_mark_lee_\d+`
- `upc_is_not_fast_\d+`
- `beans_on_toast_\d+`
- `bigred\d+`
- `terberrinse_\d+`
- `flame_of_chaos_\d+`
- `narioni_\d+`
- `jyezet_fighter_\d+`
- `{roman_numeral_regex}_proleterska_vazduhoplovna_brigada`

Here, `roman_numeral_regex` is substituted with the regular expression `m{0,4}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})`.

</details>
<details>
<summary>

#### Whitelisted Regions

</summary>

Regions are whitelisted and will never be flagged if they are:

- Suspicious, the Black Hawks, the Brotherhood of Malice, Lily, or Osiris
- Regions with a non-executive delegate
- Regions with a password
- Regions with an embassy with Antifa
- Regions with an existing delegate

</details>

## Run Site Locally

The Purée site displays all tagged regions found and allows users to filter those regions to create a list of targets. To run the site locally:

1. Clone the repository: `git clone https://github.com/esfalsa/puree.git`
2. Install Ruby dependencies: `bundle install`
3. Install Node.js dependencies: `npm install`
4. Start the development server: `bundle exec jekyll serve`

## Run Parser Locally

The Purée parser searches daily dumps for tagged regions and outputs the regions found in CSV, JSON, and XLSX formats. To run the parser locally:

1. Clone the repository: `git clone https://github.com/esfalsa/puree.git`
2. Install dependencies: `poetry install`
3. Run the parser: `poetry run python main.py`

## Contributing

Contributions are always welcome! Feel free to submit a pull request or file an issue for bug reports or feature requests.

## License

[AGPLv3](./LICENSE)
