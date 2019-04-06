# nmd-osm-tools

**This project is work in procgress** as of April 2019.

A set of tools and documentation meant to help processing Naturvårdsverket's
Nationella Marktäckedata (NMD) of Sweden.

* `remap-raster.py` - simplify GeoTIFF by replacing some values
* `process-osmxml.py` - fix warnings and simplify XML obtained on an intermediate
  stage of data import

== Data flow import overview ==

1. Import of raster and remapping of some value that will have identical tags in the end.
2. Raster undergoes vectorization with GDAL tools.
2. Smoothing of artifacts of rasterization with `v.generalize` filter of the GRASS toolset to make it look more natural.
3. Filtering out of irrelevant data: water, residential, roads etc. Mostly forests and meadows/grass are preserved.
4. Automated removal of self-intersections and duplicate nodes.
5. Removal of small objects (approximately less than 12 nodes and 120 meters in perimeter) to keep the high-frequency spatial noise low.
6. Simplification of large multipolygon outer ways to keep them under 1000 of nodes with different JOSM filters.
7. Manual splitting of larger multipolygons to keep them under 1000 nodes.

== References ==

* Import plan: [wiki](https://wiki.openstreetmap.org/wiki/WikiProject_Sweden/NMD_2018_Import_Plan)
* Mailing list discussion: [link](https://lists.openstreetmap.org/pipermail/talk-se/2019-March/003537.html)
* Source data: [link](http://mdp.vic-metria.nu/miljodataportalen/GetMetaDataURL?metaDataURL=http://mdp01.vic-metria.nu/geonetwork/srv/en/csw?request=GetRecordById%21%21%21service=CSW%21%21%21version=2.0.2%21%21%21elementSetName=full%21%21%21id=8853721d-a466-4c01-afcc-9eae57b17b39%21%21%21outputSchema=csw:IsoRecord)

