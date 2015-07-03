GeoNode Fabric Script (geonode-fabric)
================

## Description

Fabric script for managing multiple GeoNode instances, vanilla and GeoSHAPE variants.

## Installation

Follow directions at http://www.fabfile.org/installing.html to install fabric.  On Ubuntu you can most easily run, `sudo apt-get install fabric`.

Create a `geonodes.py` file in the same directory as the `fabfile.py`.  `geonodes.py` is in `.gitignore` so will not be committed.  This file includes connection and other information, so that fab commands are streamlined.

```javascript
GEONODE_INSTANCES = {
    "devgeonode": {
        "ident":  "~/auth/keys/devgeonode.pem",
        "host": "dev.geonode.example.com",
        "user": "ubuntu",
        "type": "geoshape"
    },
    "prodgeonode": {
        "ident":  "~/auth/keys/prodgeonode.pem",
        "host": "prod.geonode.example.com",
        "user": "ubuntu",
        "type": "geoshape"
    }
}
```

## Usage

Cd into the main directory with the `fabfile.py`.  When you call fab, start with `gn:geonodehost` so that the host and identity key are loaded automatically from `geonodes.py`.  A few examples:

```
fab gn:devgeonode,prodgeonode lsb_release
fab gn:devgeonode inspect_geoshape
fab gn:devgeonode restart_geoshape
fab gn:prodgeonode updatelayers_geoshape
```

## Contributing

We are currently accepting pull requests for this repository. Please provide a human-readable description with a pull request and update the README.md file as needed.

## License

Copyright (c) 2015, Patrick Dufour
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of geonode-fabric nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
