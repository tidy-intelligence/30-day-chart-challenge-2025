library(dplyr)
library(tidyr)
library(owidapi)
library(wbwdi)
library(ggplot2)
library(readr)

entities <- wdi_get_entities()

# trade_raw <- owid_get("trade-as-share-of-gdp")
# gov_spending_raw <- owid_get("historical-gov-spending-gdp")
gdp_per_capita_raw <- owid_get("gdp-per-capita-worldbank")


# gdp_per_capita_raw |>
#     filter(year == 2022) |>
#     select(entity_id, gdp_per_capita = ny_gdp_pcap_pp_kd) |>
#     left_join(
#         gov_spending_raw |>
#             filter(year == 2022) |>
#             mutate(gov_exp = expenditure / 100) |>
#             select(entity_id, gov_exp),
#         join_by(entity_id)
#     )

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
    select(name = entity_name, value)

write_csv(slope, "data/slope.csv")


# Circular ---------------------------------------------------------------

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
