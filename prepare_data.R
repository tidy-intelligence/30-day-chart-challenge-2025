library(dplyr)
library(tidyr)
library(owidapi)
library(wbwdi)
library(ggplot2)
library(readr)

entities <- wdi_get_entities()


# Fraction ---------------------------------------------------------------

gdp_per_capita_raw <- wdi_get(
    "all",
    "NY.GDP.PCAP.CD",
    start_year = 2019,
    end_year = 2019
)

# https://www.who.int/data/gho/data/indicators/indicator-details/GHO/alcohol-attributable-fractions-all-cause-deaths-(-)
fraction_raw <- readr::read_csv("data-raw/data.csv")

fraction <- fraction_raw |>
    filter(Period == 2019 & Dim2 == "All age groups (total)") |>
    select(
        entity_id = SpatialDimValueCode,
        sex = Dim1,
        value = FactValueNumeric
    ) |>
    mutate(value = value / 100) |>
    pivot_wider(id_cols = entity_id, names_from = sex, values_from = value) |>
    left_join(
        gdp_per_capita_raw |>
            select(entity_id, gdp_per_capita = value),
        join_by(entity_id)
    ) |>
    left_join(entities, join_by(entity_id)) |>
    select(
        entity_name,
        income_level_name,
        region_name,
        male = Male,
        female = Female,
        gdp_per_capita
    ) |>
    drop_na()

write_csv(fraction, "data/fractions.csv")

# Slope ------------------------------------------------------------------

# https://ourworldindata.org/grapher/female-labor-force-participation-rates-slopes
slope_raw <- owid_get("female-labor-force-participation-rates-slopes")

slope_sub <- slope_raw |>
    filter(year %in% c(2014, 2023) & !is.na(entity_id)) |>
    group_by(entity_name) |>
    filter(n() == 2) |>
    mutate(value = sl_tlf_cact_fe_ne_zs / 100)

slope_selected <- slope_sub |>
    group_by(entity_name) |>
    summarize(
        change = last(value) - first(value)
    ) |>
    arrange(-change) |>
    slice(1:5)

slope <- slope_sub |>
    inner_join(slope_selected, join_by(entity_name)) |>
    select(name = entity_name, year, value)

write_csv(slope, "data/slope.csv")


# Circular ---------------------------------------------------------------

# https://ec.europa.eu/eurostat/databrowser/view/cei_srm030/default/table?lang=en
circular_raw <- read_delim("data-raw/estat_cei_srm030.tsv", delim = "\t")

circular <- circular_raw |>
    mutate(
        entity_iso2code = substr(
            `freq,unit,geo\\TIME_PERIOD`,
            nchar(`freq,unit,geo\\TIME_PERIOD`) - 1,
            nchar(`freq,unit,geo\\TIME_PERIOD`)
        ),
        value = parse_number(`2023 `) / 100
    ) |>
    left_join(entities) |>
    mutate(
        entity_name = case_when(
            entity_iso2code == "EL" ~ "Greece",
            entity_iso2code == "20" ~ "EU",
            .default = entity_name
        )
    ) |>
    select(
        name = entity_name,
        value
    )

write_csv(circular, "data/circular.csv")


# Big or Small -----------------------------------------------------------

# https://www.sciencedirect.com/science/article/pii/S0305750X2100067X#m0045
big_or_small_raw <- read_csv2("data-raw/big_or_small_raw.csv")

big_or_small <- big_or_small_raw |>
    fill(
        `Regional or income group aggregate`,
        .direction = "down"
    ) |>
    filter(
        `Number or share of farms / agricultural area` %in%
            c("share of agricultural area (%)", "number of farms")
    ) |>
    pivot_longer(
        cols = `All sizes`:`> 1 000 ha`
    ) |>
    rename(
        entity = `Regional or income group aggregate`,
        type = `Number or share of farms / agricultural area`
    )

big_or_small <- big_or_small |>
    filter(entity == "World (129)") |>
    filter(type == "number of farms") |>
    select(name, farms = value) |>
    left_join(
        big_or_small |>
            filter(entity == "World (129)") |>
            filter(type == "share of agricultural area (%)") |>
            select(name, area = value),
        join_by(name)
    ) |>
    filter(name != "All sizes") |>
    mutate(area = area / 100)
# mutate(
#     name = case_when(
#         name == "< 1 ha" ~ "Small farms",
#         name == "> 1 000 ha" ~ "Big farms",
#         .default = "Medium farms"
#     )
# ) |>
# group_by(name) |>
# summarize(across(everything(), sum))

write_csv(big_or_small, "data/big_or_small.csv")

# Rankings ---------------------------------------------------------------

# https://dataverse.harvard.edu/dataverse/atlas

ranking_raw <- read_delim("data-raw/rankings.tab")
location_raw <- read_delim("data-raw/location_country.tab")

ranking <- ranking_raw |>
    left_join(locations_raw, join_by(country_id)) |>
    # left_join(entities, join_by(iso3_code == entity_id)) |>
    select(
        name = name_short_en,
        year,
        rank = sitc_eci_rank
    ) |>
    drop_na()

selected_ranking <- ranking |>
    filter(year == 2022) |>
    arrange(rank) |>
    slice(1:10) |>
    distinct(name)

ranking <- ranking |>
    inner_join(selected_ranking, join_by(name))

write_csv(ranking, "data/ranking.csv")
