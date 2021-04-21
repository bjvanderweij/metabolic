"""GraphQL schema definition."""

import graphene  # type: ignore
from bson.objectid import ObjectId  # type: ignore

import util


class Unit(graphene.Enum):
    KG = 'kg'
    MJ_EQ = 'MJ-Eq'
    KG_CO2_EQ = 'kg CO2-Eq'
    M2A = 'm2a'
    KG_OIL_EQ = 'kg oil-Eq'
    KG_1 = 'kg 1'
    FOUR_DC = '4-DC.'
    KG_P_EQ = 'kg P-Eq'
    KG_U235_EQ = 'kg U235-Eq'
    KG_1 = 'kg 1'
    FOUR_DB = '4-DB.'
    KG_N_EQ = 'kg N-Eq'
    KG_FE_EQ = 'kg Fe-Eq'
    M2 = 'm2'
    KG_CFC_11 = 'kg CFC-11.'
    KG_PM10_EQ = 'kg PM10-Eq'
    KG_NMVOC = 'kg NMVOC-.'
    KG_SO2_EQ = 'kg SO2-Eq'
    M3_WATER = 'm3 water-.'


class MongoObjectType(graphene.ObjectType):
    """Baseclass for ObjectTypes that represent MongoDB documents.

    Adds an ID field that resolves to the document's `_id`.
    """
    id = graphene.ID()

    async def resolve_id(parent, info):
        return parent['_id']


class Geography(MongoObjectType):
    short_name = graphene.NonNull(graphene.String)
    name = graphene.NonNull(graphene.String)


class Indicator(MongoObjectType):
    method = graphene.NonNull(graphene.String)
    category = graphene.NonNull(graphene.String)
    indicator = graphene.NonNull(graphene.String)
    unit = graphene.NonNull(Unit)

    async def resolve_indicator(parent, info):
        # I preferred indicator.name to indicator.indicator, but to
        # conform to the gql schema, I'm adding the indicator field 
        # here
        return parent['name']

class Entry(MongoObjectType):
    product_name = graphene.NonNull(graphene.String)
    unit = graphene.NonNull(Unit)
    geography = graphene.Field(Geography)
    impact = graphene.Field('schema.Impact', indicator_id=graphene.String())

    async def resolve_geography(parent, info):
        db = util.get_mongo_client()
        return await db.rivm2016.geography.find_one(
            {
                '_id': parent['geography_id']
            })

    async def resolve_impact(parent, info, indicator_id):
        db = util.get_mongo_client()
        return await db.rivm2016.impact.find_one(
            {
                'entry_id': ObjectId(parent['_id']),
                'indicator_id': ObjectId(indicator_id),
            })


class Impact(MongoObjectType):
    indicator = graphene.Field(Indicator)
    entry = graphene.Field(Entry)
    coefficient = graphene.NonNull(graphene.Float)

    async def resolve_indicator(parent, info):
        db = util.get_mongo_client()
        return await db.rivm2016.indicator.find_one({
                '_id': ObjectId(parent['indicator_id'])
            })

    async def resolve_entry(parent, info):
        db = util.get_mongo_client()
        return await db.rivm2016.entry.find_one({
                '_id': ObjectId(parent['entry_id'])
            })


class Query(graphene.ObjectType):
    indicator = graphene.Field(Indicator, id=graphene.ID())
    indicators = graphene.List(Indicator)

    entry = graphene.Field(Entry, id=graphene.ID())
    entries = graphene.List(Entry)

    impact = graphene.Field(
            Impact,
            entry_id=graphene.ID(),
            indicator_id=graphene.ID()
        )

    async def resolve_indicators(parent, info):
        db = util.get_mongo_client()
        return await db.rivm2016.indicator.find().to_list(None)

    async def resolve_indicator(parent, info, id):
        db = util.get_mongo_client()
        return await db.rivm2016.indicator.find_one(
            {
                '_id': ObjectId(id)
            })

    async def resolve_entries(parent, info):
        db = util.get_mongo_client()
        return await db.rivm2016.entry.find().to_list(None)

    async def resolve_entry(parent, info, id):
        db = util.get_mongo_client()
        return await db.rivm2016.entry.find_one(
            {
                '_id': ObjectId(id)
            })

    async def resolve_impact(parent, info, entry_id, indicator_id):
        db = util.get_mongo_client()
        return await db.rivm2016.impact.find_one(
            {
                'entry_id': ObjectId(entry_id),
                'indicator_id': ObjectId(indicator_id),
            })
