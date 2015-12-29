-- DROP SCHEMA IF EXISTS view_osmaxx;

DROP VIEW if exists view_osmaxx.address_p;
DROP VIEW if exists view_osmaxx.adminarea_a;
DROP VIEW if exists view_osmaxx.boundary_l;
DROP VIEW if exists view_osmaxx.building_a;
DROP VIEW if exists view_osmaxx.geoname_l;
DROP VIEW if exists view_osmaxx.geoname_p;
DROP VIEW if exists view_osmaxx.landuse_a;
DROP VIEW if exists view_osmaxx.military_a;
DROP VIEW if exists view_osmaxx.military_p;
DROP VIEW if exists view_osmaxx.misc_l;
DROP VIEW if exists view_osmaxx.natural_a;
DROP VIEW if exists view_osmaxx.natural_p;
DROP VIEW if exists view_osmaxx.nonop_l;
DROP VIEW if exists view_osmaxx.poi_a;
DROP VIEW if exists view_osmaxx.poi_p;
DROP VIEW if exists view_osmaxx.pow_a;
DROP VIEW if exists view_osmaxx.pow_p;
DROP VIEW if exists view_osmaxx.railway_l;
DROP VIEW if exists view_osmaxx.road_l;
DROP VIEW if exists view_osmaxx.route_l;
DROP VIEW if exists view_osmaxx.traffic_a;
DROP VIEW if exists view_osmaxx.traffic_p;
DROP VIEW if exists view_osmaxx.transport_a;
DROP VIEW if exists view_osmaxx.transport_p;
DROP VIEW if exists view_osmaxx.utility_a;
DROP VIEW if exists view_osmaxx.utility_p;
DROP VIEW if exists view_osmaxx.utility_l;
DROP VIEW if exists view_osmaxx.water_p;
DROP VIEW if exists view_osmaxx.water_a;
DROP VIEW if exists view_osmaxx.water_l;

DROP SCHEMA IF EXISTS view_osmaxx;

-- DROP SCHEMA IF EXISTS osmaxx;

DROP TABLE if exists osmaxx.address_p;
DROP TABLE if exists osmaxx.adminarea_a;
DROP TABLE if exists osmaxx.boundary_l;
DROP TABLE if exists osmaxx.building_a;
DROP TABLE if exists osmaxx.landuse_a;
DROP TABLE if exists osmaxx.military_a;
DROP TABLE if exists osmaxx.military_p;
DROP TABLE if exists osmaxx.misc_l;
DROP TABLE if exists osmaxx.natural_a;
DROP TABLE if exists osmaxx.natural_p;
DROP TABLE if exists osmaxx.nonop_l;
DROP TABLE if exists osmaxx.geoname_l;
DROP TABLE if exists osmaxx.geoname_p;
DROP TABLE if exists osmaxx.pow_a;
DROP TABLE if exists osmaxx.pow_p;
DROP TABLE if exists osmaxx.transport_a;
DROP TABLE if exists osmaxx.transport_p;
DROP TABLE if exists osmaxx.railway_l;
DROP TABLE if exists osmaxx.road_l;
DROP TABLE if exists osmaxx.route_l;
DROP TABLE if exists osmaxx.traffic_a;
DROP TABLE if exists osmaxx.traffic_p;
DROP TABLE if exists osmaxx.utility_a;
DROP TABLE if exists osmaxx.utility_p;
DROP TABLE if exists osmaxx.utility_l;
DROP TABLE if exists osmaxx.water_p;
DROP TABLE if exists osmaxx.water_a;
DROP TABLE if exists osmaxx.water_l;

DROP SCHEMA IF EXISTS osmaxx;

-- CREATE SCHEMA
CREATE SCHEMA osmaxx;
CREATE SCHEMA view_osmaxx;
