Repository holding Kubernetes JSON schemas, build according to: https://github.com/instrumenta/kubernetes-json-schema/issues/26:
---

> I worked around missing schemas for 1.19 by generating them on my own. This seems to work at first glance, although I don't have much prior experience with kubeval:

> In Linux (or WSL):

>     # install tooling to generate the schemas
>     sudo apt install python-pip
>     export PYTHONHTTPSVERIFY=0 # this is only because I had cert issues
>     pip install openapi2jsonschema

>     # generate a folder with schema files for a specific version (1.19.3 in this case)
>     openapi2jsonschema -o "v1.19.3-standalone-strict" --kubernetes --stand-alone --strict https://raw.githubusercontent.com/kubernetes/kubernetes/v1.19.3/api/openapi-spec/swagger.json

>     # now fork this repo, add the generated files, commit, push

---

First install openapi2jsonschema with `pip install openapi2jsonschema`.

Then run the command with added --expanded switch to create all relevant files for the release (here v1.20.0):

    openapi2jsonschema -o "v1.20.0-standalone-strict" --expanded --kubernetes --stand-alone --strict https://raw.githubusercontent.com/kubernetes/kubernetes/v1.20.0/api/openapi-spec/swagger.json

> Note that this command might produce many errors like:

`An error occured processing mutatingwebhook: URLError: <urlopen error [WinError 3] Das System kann den angegebenen Pfad nicht finden: '\\v1.22.0-standalone-strict\\_definitions.json'>`

It seems as if those don't corrupt the result and can be ignored.