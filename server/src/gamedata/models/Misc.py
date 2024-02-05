from sqlalchemy import ARRAY, JSON, Boolean, Column, Float, Integer, String
from sqlalchemy.orm import relationship

from ..utils import Category
from .Item import Item


class MiscItem(Item):
    __tablename__ = 'misc_items'
    
    count = Column(Integer, nullable=True)
    category = Column(String, nullable=True)
    description = Column(String, nullable=True)
    excludeFromCodex = Column(Boolean, nullable=True)
    imageName = Column(String, nullable=True)
    masterable = Column(Boolean, nullable=True)
    name = Column(String, nullable=True)
    tradable = Column(Boolean, nullable=True)
    type = Column(String, nullable=True)
    uniqueName = Column(String, nullable=True)
    showInInventory = Column(Boolean, nullable=True)
    itemCount = Column(Integer, nullable=True)
    probability = Column(Float, nullable=True)
    rarity = Column(String, nullable=True)
    rewardName = Column(String, nullable=True)
    tier = Column(Integer, nullable=True)
    fusionPoints = Column(Integer, nullable=True)
    buildPrice = Column(Integer, nullable=True)
    buildQuantity = Column(Integer, nullable=True)
    buildTime = Column(Integer, nullable=True)
    consumeOnBuild = Column(Boolean, nullable=True)
    criticalChance = Column(Integer, nullable=True)
    criticalMultiplier = Column(Integer, nullable=True)
    fireRate = Column(Integer, nullable=True)
    masteryReq = Column(Integer, nullable=True)
    omegaAttenuation = Column(Integer, nullable=True)
    procChance = Column(Integer, nullable=True)
    productCategory = Column(String, nullable=True)
    skipBuildTimePrice = Column(Integer, nullable=True)
    totalDamage = Column(Integer, nullable=True)
    accuracy = Column(Integer, nullable=True)
    primeOmegaAttenuation = Column(Float, nullable=True)
    blockingAngle = Column(Integer, nullable=True)
    comboDuration = Column(Integer, nullable=True)
    followThrough = Column(Integer, nullable=True)
    heavyAttackDamage = Column(Integer, nullable=True)
    heavySlamAttack = Column(Integer, nullable=True)
    heavySlamRadialDamage = Column(Integer, nullable=True)
    heavySlamRadius = Column(Integer, nullable=True)
    range = Column(Float, nullable=True)
    slamAttack = Column(Integer, nullable=True)
    slamRadialDamage = Column(Integer, nullable=True)
    slamRadius = Column(Integer, nullable=True)
    slideAttack = Column(Integer, nullable=True)
    windUp = Column(Float, nullable=True)
    magazineSize = Column(Integer, nullable=True)
    binCapacity = Column(Integer, nullable=True)
    binCount = Column(Integer, nullable=True)
    durability = Column(Integer, nullable=True)
    fillRate = Column(Integer, nullable=True)
    repairRate = Column(Integer, nullable=True)
    stancePolarity = Column(String, nullable=True)
    
    # define relationships
    drops = relationship('Drop')
    components = relationship('Item')

    # Define nullable arrays
    polarities = Column(ARRAY(String), nullable=True)
    tags = Column(ARRAY(String), nullable=True)

    # Define nullable JSON fields
    attacks = Column(JSON, nullable=True)
    damage = Column(JSON, nullable=True)
    damagePerShot = Column(JSON, nullable=True)
    introduced = Column(JSON, nullable=True)
    
    # Define nullable additional JSON fields
    components = Column(JSON, nullable=True)


    # Set the polymorphic_identity to match the category 'Glyphs'
    __mapper_args__ = {
        "polymorphic_identity": Category.Misc.value,
    }