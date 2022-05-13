hasSubProp = {
    # "prop": {
    #   "subprop":"name_value",
    #   "subprop":"name_value"
    # },
    "cpmeta:fundingInfoProp": {
        "cpmeta:funderIdentifier": "id",  # xsd:string
        "cpmeta:funderIdentifierType": "id_type",  # rdfs:Datatype
        "cpmeta:awardNumber": "award_number",  # xsd:string
        "cpmeta:awardURI": "award_uri",  # xsd:anyURI
        "cpmeta:awardTitle": "award_title",  # xsd:string
    },
    "cpmeta:hasExtraRoleInfo": {
        "cpmeta:hasAttributionWeight": "attribution_weight",  # xsd:integer
    },
    "cpmeta:hasFormatSpecificMetadata": {
        "wdcgg:CONTACT%20POINT": "contact_point",  #
        "wdcgg:CONTRIBUTOR": "contributor",  #
        "wdcgg:MEASUREMENT%20METHOD": "measurement_method",  #
        "wdcgg:MEASUREMENT%20SCALE": "measurement_scale",  #
        "wdcgg:MEASUREMENT%20UNIT": "measurement_unit",  #
        "wdcgg:OBSERVATION%20CATEGORY": "observation_category",  #
        "wdcgg:PARAMETER": "parameter",  #
        "wdcgg:SAMPLING%20TYPE": "sampling_type",  #
        "wdcgg:TIME%20INTERVAL": "time_interval",  #
    },
    "cpmeta:hasPolicy": {
        "cpmeta:hasHideFromSearchPolicy": "hide_from_search_policy",  # xsd:boolean
        "cpmeta:hasSkipPidMintingPolicy": "skip_pid_minting_policy",  # xsd:boolean
        "cpmeta:hasSkipStoragePolicy": "skip_storage_policy",  # xsd:boolean
    },
    "cpmeta:hasStationSpecificParam": {
        "cpmeta:country": "country",  # xsd:string
        "cpmeta:countryCode": "country_code",  # xsd:string
        "cpmeta:hasStationClass": "class",  # rdfs:Datatype
        "cpmeta:hasStationId": "id",  # xsd:string
        "cpmeta:hasOperationalPeriod": "operational_period",  # xsd:string
        "cpmeta:hasLabelingDate": "label_date",  # xsd:date
        "cpmeta:hasMeanAnnualTemp": "mean_annual_temperature",  # xsd:float
        "cpmeta:hasMeanAnnualPrecip": "mean_annual_precip",  # xsd:float
        "cpmeta:hasMeanAnnualRadiation": "mean_annual_radiation",  # xsd:float
        "cpmeta:hasTimeZoneOffset": "time_zone_offset",  # xsd:integer
    },
    "cpmeta:hasStringId": {
        "cpmeta:hasOrcidId": "orcidid",  # xsd:string
        "cpmeta:hasStationId": "stationid",  # xsd:string
        "cpmeta:hasTcId": "tcid",  # xsd:string
        "cpmeta:hasWigosId": "wigosid",  # xsd:string
    },
    "cpmeta:hasTcId": {
        "cpmeta:hasAtcId": "atcid",  # xsd:string
        "cpmeta:hasEtcId": "etcid",  # xsd:string
        "cpmeta:hasOtcId": "otcid",  # xsd:string
    },
    "cpmeta:hasVariable": {
        "cpmeta:hasColumn": "dataset_column",  # cpmeta/TabularDatasetSpec
    },
    "cpmeta:hasVariableTitle": {
        "cpmeta:hasColumnTitle": "column_title",  # xsd:string
    },
    "cpmeta:isOptionalVariable": {
        "cpmeta:isOptionalColumn": "is_optional_column",  # xsd:boolean
    },
    "cpmeta:isRegexVariable": {
        "cpmeta:isRegexColumn": "is_regex_column",  # xsd:boolean
    },
    "cpmeta:latlongs": {
        "cpmeta:hasLatitude": "latitude",  # xsd:double
        "cpmeta:hasLongitude": "longitude",  # xsd:double
        "cpmeta:hasEasternBound": "eastern_bound",  # xsd:double
        "cpmeta:hasNorthernBound": "northern_bound",  # xsd:double
        "cpmeta:hasSouthernBound": "southern_bound",  # xsd:double
        "cpmeta:hasWesternBound": "western_bound",  # xsd:double
    },
    "geosparql:hasGeometry": {
        "cpmeta:hasSpatialCoverage": "location",  # cpmeta/DataObject | cpmeta/Station | geosparql#Feature
    },
    "geosparql:hasSerialization": {
        "cpmeta:asGeoJSON": "geojson",  # string
    },
    "prov:atLocation": {
        "cpmeta:hasSamplingPoint": "sampling_point",  # cpmeta.Position, cpmeta.DataAcquisition
        "cpmeta:locatedAt": "located_at",  # geosparql#Feature
        "cpmeta:operatesOn": "station_Site",  # cpmeta/Site
        "cpmeta:wasPerformedAt": "geofeature",  # geosparql#Feature
    },
    "prov:wasAssociatedWith": {
        "cpmeta:wasHostedBy": "organisation",  # organization
        "cpmeta:wasPerformedBy": "performed_by",
        "cpmeta:wasParticipatedInBy": "participated_in_by",
    },
    "prov:wasAssociatedWith": {
        "cpmeta:wasHostedBy": "organisation",  # organization
        "cpmeta:wasPerformedBy": "performed_by",
        "cpmeta:wasParticipatedInBy": "participated_in_by",
    },
    "prov:wasRevisionOf": {
        "cpmeta:isNextVersionOf": "NextVersionOf",  # prov#Entity
        # Warning: linked to:
        # - superIcpObj.py:_getSubAttr(): elif k in 'NextVersionOf':
    },
    "prov:wasGeneratedBy": {
        "cpmeta:wasAcquiredBy": "acquisition",  # cpmeta/DataAcquisition
        "cpmeta:wasProducedBy": "production",  # cpmeta/DataProduction
        "cpmeta:wasSubmittedBy": "submission",  # cpmeta/DataSubmission
    },
    "schema:image": {
        "cpmeta:hasDepiction": "depiction",  #
        "cpmeta:hasIcon": "icon",  #
        "cpmeta:hasMarkerIcon": "marker_icon",  #
    },
    "skos:broader": {
        "cpmeta:broaderEcosystem": "broader_ecosystem",  # cpmeta/EcosystemType
    },
    "skos:closeMatch": {
        "skos:exactMatch": "exact_match",  # skos/core#Concept
    },
    "ssn:hasSubSystem": {
        "cpmeta:hasInstrumentComponent": "component",  # cpmeta/Instrument
    },
    "terms:bibliographicCitation": {
        "cpmeta:hasAssociatedPublication": "associated_publication",  # xsd:anyURI
        "cpmeta:hasDocumentationUri": "documentation_uri",  # xsd:anyURI
    },
    "terms:format": {
        "cpmeta:hasEncoding": "encoding",  # cpmeta/ObjectEncoding
        "cpmeta:hasFormat": "format",  # cpmeta/ObjectFormat
    },
    "terms:title": {
        "cpmeta:hasName": "name",  # xsd:string
        "cpmeta:hasVariableTitle": "variable_title",  # xsd:string
    },
}
