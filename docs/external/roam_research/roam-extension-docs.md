- **Introduction**
    - Your extension's code runs alongside Roam's code, the same as [[roam/js]], with full access to the dom and the [[Roam Alpha API]], and a new [[Roam Depot/Extension API]]
    - Every update to your extension will be submitted and reviewed for security by Roam's team through the [github repo](https://github.com/Roam-Research/roam-depot)
    - In an effort to support authors and encourage ongoing maintenance of extensions, Roam is dedicating a portion of our revenue to extension authors.
        - The amount and way we distribute funds is subject to change
        - If you are interested in receiving payouts, sign up with stripe in extension settings and add your account ID to your extension's metadata
            - **Please complete the process in full and make sure your account is enabled submitting an extension with the account attached. We can only send funds if your account is fully filled out. You can contact Josh on slack if you do not know if your account is enabled or not.**
                - We should be able to support authors in all of the countries listed in https://stripe.com/docs/connect/cross-border-payouts (not the preview ones yet, but if you are in one of those contact us first and we can try to get it working).
            - Legally, if you make more than $600 per year from Roam and live in the US, you are expected to pay taxes on it and can ask Roam for a 1099 form
        - Paid extensions do not exist yet, but in the future we hope to add them. You may implement your own payment system for an extension, but this will disqualify you from payouts from Roam
- **Code Guidelines**
    - Your extension should export as default a map with `onload` and `onunload` functions
        - All state setup in `onload` should be removed in `onunload`.
        - `onload` receives an object with the [[Roam Depot/Extension API]] in it
        - ```javascript
          export default {
            onload: ({extensionAPI}) => {},
            onunload: () => {}
          };
          ```
    - Roam APIs
        - You'll have access to two different APIs for development, the [[Roam Alpha API]] and the [[Roam Depot/Extension API]]
            - Why two?
                - The [[Roam Alpha API]] was developed before the existence of Roam Depot, and modifying that to fit the needs of Roam Depot would break existing [[roam/js]] extensions
                    - Particularly, for Roam Depot, we can pre-fill functions with information about your extension and automatically remove components when your extension is uninstalled
                - Eventually, everything will be duplicated inside of the [[Roam Depot/Extension API]] for ease of use
            - Please read the documentation for these, there is likely already a method for what you need and if there isn't let us know in the #developers channel on slack
    - User Interface
        - Extensions should prefer using [blueprintjs](https://blueprintjs.com/docs/versions/3/) components to match Roam's style
    - Styles
        - Extensions should prefix css classes with a unique identifier such that it won't conflict with roam or other extensions.
            - Example::
                - Roam uses `rm-` in front of all our css classes, `rm-modal`
        - The majority of tailwind css is included with Roam
    - Dependencies
        - Your dependencies will be scrutinized heavily, some general guidelines
            - If you can do it without a dependency, do not use a dependency
            - Only use trustworthy dependencies, extensions will be rejected if our team decides one of your dependencies is untrustworthy
        - Roam exports a number of dependencies for extensions to use. Extensions must use these instead of bundling their own version or a library similar to one of these.
            - Your bundler may support `import` from the window object to make it easier to import global dependencies
                - [webpack example](https://github.com/dvargas92495/roamjs-scripts/blob/main/src/index.ts#L122-L126)
            - Alternatively, you access them from the window object
            - Sync dependencies
                - Dependencies bundled with Roam core will be provided on the window object
                - {{table}}
                    - **Package Name**
                        - **Version**
                            - **Global Var**
                    - `react`
                        - `18.2.0`
                            - `window.React`
                    - `react-dom`
                        - `18.2.0`
                            - `window.ReactDOM`
                    - `@blueprintjs/core`
                        - `^3.50.4`
                            - `window.Blueprint.Core`
                    - `@blueprintjs/select`
                        - `^3.18.6`
                            - `window.Blueprint.Select`
                    - `@blueprintjs/datetime`
                        - `^3.23.14`
                            - `window.Blueprint.DateTime`
                    - `chrono-node`
                        - `^2.3.2`
                            - `window.ChronoNode`
                    - `idb`
                        - ` 7.1.1`
                            - `window.idb`
                    - `nanoid`
                        - `^2.0.4`
                            - `window.Nanoid`
                    - `file-saver`
                        - `^2.0.2`
                            - `window.FileSaver`
                    - `crypto-js`
                        - `^3.1.9-1`
                            - `window.CryptoJS`
                    - `tslib`
                        - `2.2.0`
                            - `TSLib`
            - Async dependencies
                - Some of Roam's dependencies are loaded only when a user uses them, your extension should do the same thing
                    - We understand dynamically loading is pretty difficult for a beginner, if that is you, you can ask us for help or for an exception to this rule
                - {{table}}
                    - **Package Name**
                        - **Version**
                            - **Global Var**
                    - `marked-react`
                        - `^1.1.2`
                            - `RoamLazy.MarkedReact`
                    - `marked`
                        - `4.3.0`
                            - `RoamLazy.Marked`
                    - `jszip`
                        - `^3.10.0`
                            - `RoamLazy.JSZip`
                    - `cytoscape`
                        - `^3.7.2`
                            - `RoamLazy.Cytoscape`
                    - `insect.js`
                        - `5.6.0`
                            - `RoamLazy.Insect`
    - Offline
        - Extensions will run offline, your extension doesn't have to work offline but it should be aware it could be running without network connection and handle that accordingly
    - Allowed languages
        - Typescript, Javascript, or Clojurescript
- **Local Development**
    - To develop locally, you'll have to use this url [https://relemma-git-roam-app-store.roamresearch.com](https://relemma-git-roam-app-store.roamresearch.com/) (until we launch)
    - Visit a graph, open up settings, and go to the extensions tab
    - Then click enable developer mode
        - ![](https://firebasestorage.googleapis.com/v0/b/firescript-577a2.appspot.com/o/imgs%2Fapp%2Fdeveloper-documentation%2FHwNXRGTwD-.png?alt=media&token=23259c21-321c-4687-b2aa-0ce974b23290)
    - Then load extension
        - ![](https://firebasestorage.googleapis.com/v0/b/firescript-577a2.appspot.com/o/imgs%2Fapp%2Fdeveloper-documentation%2FCxT8jRodC9.png?alt=media&token=dfb0e961-33d1-449d-b39c-724474b92aa9)
    - and choose the folder on your computer which contains `extension.js` / `extension.css`
    - To reload the extension you can use the key command `control-d control-r`, which will call your extension's `unload` function, load the new code, and call `onload`
        - Note that this key command reloads all loaded developer extensions
            - You can also reload extensions from the extensions tab in settings
    - If your state isn't properly removed in `unload` then you can reload the page and hit `control-d control-r` to completely clear the state
- **Submitting an extension**
    - Create a github repo for your extension
    - Inside your repository
        - Provide
            - README.md (required)
                - This will be displayed to users inside of Roam, include any relevant long description for your extension
            - extension.js (required)
            - extension.css (optional)
            - CHANGELOG.md (optional)
        - If your extension bundles dependencies and requires a build step
            - Provide a `build.sh` file
            - The `build.sh` file will be invoked before looking for extension.js (required) or extension.css (optional)
            - The environment it’ll be invoked in is ubuntu-20.04 from Github Actions. Consult [this](https://github.com/actions/virtual-environments/blob/main/images/linux/Ubuntu2004-Readme.md) to see what is available. (npm and yarn are available)
            - If your build script requires anything extra (e.g. libraries from NPM), it should download them as a part of build.sh execution.
        - If not and your extension is a simple javascript file, then you can write all of your code in extension.js (required)
    - Fork https://github.com/Roam-Research/roam-depot
        - Create metadata file in extensions/<your username>/<your repo>.json
        - Example
            - `extensions/tonsky/roam-calculator.json`
            - with the following content
            - ```javascript
              {
                "name": "Test Extension 1",
                "short_description": "Prints 'Test message 1'",
                "author": "Nikita Prokopov",
                "tags": ["print", "test"], //optional
                "source_url": "https://github.com/tonsky/roam-calculator",
                "source_repo": "https://github.com/tonsky/roam-calculator.git",
                "source_commit": "d5ecd16363975b2e7a097d46e5f411c95e16682d",
                "stripe_account": "acct_1LGASrQVCl6NYjck" // optional only include if you want to be eligible for payouts from Roam
              }
              ```
        - Then make a Pull Request with this change. After it’s merged, your extension will be published in the Roam Marketplace.
