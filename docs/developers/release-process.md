# Release process

I'd wish the release process to be more automated, but for now it's still a
few manual steps.

## Prepare the PR for the new release

### Edit files

1. Find the next version, using semantic versioning (e.g. `1.2.3`), depending on
   the changes in the changelog
2. Execute `./new_release NEW_VERSION` (replace `NEW_VERSION` with the new version)
3. Update the AppData release notes in data/io.github.mightycreak.Diffuse.appdata.xml.in:
   - Look for the empty `<p>` tag under the new `<release>` tag
   - Add a paragraph to sum the release in one sentence (e.g. highlights, ...)
   - Paste the changes from CHANGELOG.md and adapt it to HTML (see other
     releases in the file)

### Create branch, PR and merge

1. Create a new branch (e.g. `release-1.2.3`)
2. Create a new PR
3. When everything's green: merge the PR

## Create new release on GitHub

1. Create a new release on GitHub's [new release page](https://github.com/MightyCreak/diffuse/releases/new):
   - Choose a tag: `v` followed with the new version (e.g. `v1.2.3`)
   - Release title: the tag (e.g. `v1.2.3`)
   - Description:
     - For the first paragraph, paste the first paragraph from the release notes
     - For the second paragraph, got to [CHANGELOG.md](https://github.com/MightyCreak/diffuse/blob/main/CHANGELOG.md)
       and copy the URL anchor to the new release, then add this sentence
       (adapt the changelog link):

       ```text
       For a more detailed list of changes, see the
       [changelog](https://github.com/MightyCreak/diffuse/blob/main/CHANGELOG.md#xyz---yyyy-mm-dd).
       ```

2. Publish release

## Create new release on Flatpak

1. Clone the Flathub repository: <https://github.com/flathub/io.github.mightycreak.Diffuse>
2. Copy the contents of Diffuse's `io.github.mightycreak.Diffuse.yml` to Flathub's
3. Keep Flathub's `config-opts` and `sources` sections
4. In `sources` section, change the `commit` and `tag`
5. Create commit with changes and push to `master`
6. Check the build on Flathub: <https://flathub.org/builds/>
7. When it's done and successful, publish the build
