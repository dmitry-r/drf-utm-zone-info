--------------------
-- drinking water --
--------------------
INSERT INTO osmaxx.poi_a
 SELECT osm_id as osm_id,
	osm_timestamp as lastchange,
	CASE
	 WHEN osm_id<0 THEN 'R' -- Relation
	 ELSE 'W' 		-- Way
	 END AS geomtype,
	ST_Multi(way) AS geom,
	'miscpoi' as aggtype,
-- Combining the different tags in drinking water into different categories --
	case
	 when amenity='fountain' then
		case
		 when drinkable='yes' then 'drinkable_fountain'
		 else 'fountain'
		end
 	 when man_made='water_well' then
		case
		 when drinkable='yes' then 'drinkable_well'
		 else 'water_well'
		end
	end as type,
	name as name,
	"name:en" as name_en,
	"name:fr" as name_fr,
	"name:es" as name_es,
	"name:de" as name_de,
	int_name as name_int,
	transliterate(name) as label,
	cast(tags as text) as tags,
	website as website,
	wikipedia as wikipedia,
	phone as phone,
	"contact:phone" as contact_phone,
	opening_hours as opening_hours,
	cuisine as cuisine,
	"access" as "access",
	brand as brand,
	"tower:type" as tower_type
  FROM osm_polygon
  WHERE amenity='fountain' or man_made='water_well';
