# Release process

I'd wish the release process to be more automated, but for now it's still a
few manual steps.

## Prepare the PR for the new release

1. Find the next version, using semantic versioning, depending on the changes
   in the changelog
2. Find and replace the old version with the new version in some files:
   - meson.build
   - windows-installer/build.py
   - windows-installer/diffuse.iss
   - windows-installer/diffuse.new.iss
3. Update CHANGELOG.md
   - Add new line under `## Unreleased` following this syntax: `## x.y.z - YYYY-MM-DD`
   - Copy the content of the changes for this release
4. Update AppData release notes in data/io.github.mightycreak.Diffuse.appdata.xml.in:
   - Create a new `<release>` tag under `<releases>`, fill the `version` and
     `date` attributes
   - Create a new `<description>` tag under the new `<release>` tag
   - Add one paragraph to sum the release in one sentence (e.g. highlights, ...)
   - Paste the changes from the changelog and adapt it to HTML
5. Create new branch and PR

## Create new release on GitHub

1. When everything's green: merge the PR
2. Create a new release on GitHub's [new release page](https://github.com/MightyCreak/diffuse/releases/new):
   - Choose a tag: `v` followed with the new version (e.g. `v1.2.3`)
   - Release title: the tag (e.g. `v1.2.3`)
   - Description:
     - For the first paragraph, paste the first paragraph from the release notes
     - For the second paragraph, got to [CHANGELOG.md](https://github.com/MightyCreak/diffuse/blob/master/CHANGELOG.md)
       and copy the URL anchor to the new release, then add this sentence
       (adapt the changelog link):  
       > For a more detailed list of changes, see the
       > [changelog](https://github.com/MightyCreak/diffuse/blob/master/CHANGELOG.md#xyz---yyyy-mm-dd).
3. Publish release

## Create new release on Flatpak

1. Clone the Flathub repository: https://github.com/flathub/io.github.mightycreak.Diffuse
2. Copy the contents of Diffuse's `io.github.mightycreak.Diffuse.yml` to Flathub's
3. Keep Flathub's `config-opts` and `sources` sections
4. In `sources` section, change the `commit` and `tag`
5. Create commit with changes and push to `master`
6. Check the build on Flathub: https://flathub.org/builds/
7. When it's done and successful, publish the build
