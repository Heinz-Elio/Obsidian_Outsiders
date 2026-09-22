# IU7/00_overview

## Outsiders
Source: IU7/00_overview/overview.md

#### Outsiders

```dataview
TABLE alive, ranger, military, process_srune
FROM "Setting/IU7/01_character" // full path
WHERE entity_type = "outsider"
```
#### Rangers

```dataview
TABLE entity_type
FROM "Setting/IU7/01_character" // full path
WHERE ranger = true
```
#### Dead

```dataview
TABLE entity_type,alive
FROM "Setting/IU7/01_character" // full path
WHERE alive = false
```
#### Military

```dataview
TABLE entity_type
FROM "Setting/IU7/01_character" // full path
WHERE military = true
```
#### Srune

```dataview
TABLE entity_type
FROM "Setting/IU7/01_character" // full path
WHERE process_srune = true
```
#### Kingdom

```dataview
TABLE type, subtype
FROM "Setting/IU7/08_organization" // full path
WHERE subtype = "kingdom"
```
