# Purée

[Purée](https://esfalsa.github.io/puree) is an easy-to-use website that flags NationStates regions which may have been tagged.

## Features

Purée allows you to…

- Identify regions that may have been tagged
- Track the number of regions found over time
- Generate lists of regions to detag

## Flagging Criteria

Currently, Purée flags regions with:

- Links in the WFE to the Brotherhood of Malice, the Black Hawks, Valle de Arena, or Lily
- Embassies are open or requested (not closing or rejected) with the Black Hawks, the Brotherhood of Malice, Valle de Arena, Red Front, or Plum Island
- A regional officer position named "Raider Unity", "Thorn1000", "JOIN TBH", "Join %%Lily%%", or "Lily"

Regions meeting these criteria are whitelisted if they are:

- Suspicious, the Black Hawks, the Brotherhood of Malice, Lily, and Osiris
- Regions with a non-executive delegate
- Regions with a password
- Regions with an embassy with Antifa
- Regions with an existing delegate

## Run Locally

1. Clone the repository: `git clone https://github.com/esfalsa/puree.git`
2. Install Ruby dependencies: `bundle install`
3. Install Node.js dependencies: `npm install`
4. Start the development server: `bundle exec jekyll serve`

## Contributing

Contributions are always welcome! Feel free to submit a pull request or file an issue for bug reports or feature requests.

## License

[AGPLv3](./LICENSE)
