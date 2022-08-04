import random

class Gun:
    def __init__(self, klass, type, name):
        self.klass = klass
        self.name = name
        tiers = class_info[self.klass][type][name]['tiers']
        self.tiers = [(random.randrange(m) + 1) for m in tiers]
        self.overclock = random.choice(class_info[self.klass][type][name]['overclocks'])
    
    def __str__(self):
        return f'{self.name} - {self.tiers}\n    **Overclock:** {self.overclock}'

class Equipment():
    def __init__(self, klass, id):
        self.name = class_info[klass]['equipment'][id]['name']
        tiers = class_info[klass]['equipment'][id]['tiers']
        self.tiers = [(random.randrange(m) + 1) for m in tiers]

    def __str__(self):
        return f'**{self.name}**: {self.tiers}'

class Build:
    def __init__(self, klass=None):
        if (klass and not klass in class_info):
            return
        self.klass = klass if klass else random.choice(list(class_info.keys()))
        primary = random.choice(list(class_info[self.klass]['primary'].keys()))
        self.primary = Gun(self.klass, 'primary', primary)
        secondary = random.choice(list(class_info[self.klass]['secondary'].keys()))
        self.secondary = Gun(self.klass, 'secondary', secondary)
        self.equipment1 = Equipment(self.klass, 0)
        self.equipment2 = Equipment(self.klass, 1)
        armor_tiers = class_info[self.klass]['armor']
        self.armor = [(random.randrange(m) + 1) for m in armor_tiers]
        self.throwable = random.choice(class_info[self.klass]['throwables'])

        self.pickaxe = [(random.randrange(m) + 1) for m in pickaxe]

        self.active_perks = ', '.join(random.sample(perks['active'], 2))
        self.passive_perks = ', '.join(random.sample(perks['passive'], 3))

    def __str__(self):
        return f'**Randon build for {self.klass.capitalize()}**\n\n**Primary:** {self.primary}\n**Secondary:** {self.secondary}\n{self.equipment1}\n{self.equipment2}\n**Pickaxe:** {self.pickaxe}\n**Armor:** {self.armor}\n**Throwable:** {self.throwable}\n\n**Passive Perks:** {self.active_perks}\n**Active Perks:** {self.passive_perks}'

def is_valid_class(klass):
    return klass == None or klass in class_info

class_info = {
    'driller': {
        'primary': {
            'CRSPR Flamethrower': {
                'tiers': [2, 3, 3, 3, 2],
                'overclocks': ['Lighter Tanks', 'Sticky Additive', 'Compact Feed Valves', 'Fuel Stream Diffuser', 'Face Melter', 'Sticky Fuel'],
            },
            'Cryo Cannon': {
                'tiers': [3, 3, 2, 3, 2],
                'overclocks': ['Improved Thermal Efficiency', 'Tuned Cooler', 'Flow Rate Expansion', 'Ice Spear', 'Ice Storm', 'Snowball'],
            },
            'Corrosive Sludge Pump': {
                'tiers': [3, 3, 2, 2, 2],
                'overclocks': ['Hydrogen Ion Additive', 'AG Mixture', 'Volatile Impact Mixture', 'Disperser Compound', 'Goo Bomber Special', 'Sludge Blast'],
            },
        },
        'secondary': {
            'Subata 120': {
                'tiers': [3, 2, 3, 2, 2],
                'overclocks': ['Chain Hit', 'Homebrew Powder', 'Oversized Magazine', 'Automatic Fire', 'Explosive Reload', 'Tranquilizer Rounds'],
            },
            'Experimental Plasma Charger': {
                'tiers': [3, 2, 3, 3, 3],
                'overclocks': ['Energy Rerouting', 'Magnetic Cooling Unit', 'Heat Pipe', 'Heavy Hitter', 'Overcharger', 'Persistent Plasma'],
            },
            'Colette Wave Cooker': {
                'tiers': [3, 3, 2, 2, 3],
                'overclocks': ['Liquid Cooling System', 'Super Focus Lens', 'Diffusion Ray', 'Mega Power Supply', 'Blistering Necrosis', 'Gamma Contamination'],
            },
        },
        'equipment': [
            {
                'name': 'Reinforced Power Drills',
                'tiers': [3, 2, 1, 2],
            },
            {
                'name': 'Satchel Charge',
                'tiers': [3, 1, 2, 3],
            },
        ],
        'armor': [3, 2, 1, 3],
        'throwables': ['Impact Axe', 'High Explosive Grenade', 'Neurotoxin Grenade'],
    },
    'engineer': {
        'primary': {
            '"Warthog" Auto 210': {
                'tiers': [2, 3, 3, 2, 2],
                'overclocks': ['Stunner', 'Light-Weight Magazines', 'Magnetic Pellet Alignment', 'Cycle Overload', 'Mini Shells'],
            },
            '"Stubby" Voltaic SMG': {
                'tiers': [3, 3, 2, 2, 2],
                'overclocks': ['Super-Slim Rounds', 'Well Oiled Machine', 'EM Refire Booster', 'Light-Weight Rounds', 'Turret Arc', 'Turret EM Discharge'],
            },
            'LOK-1 Smart Rifle': {
                'tiers': [2, 3, 3, 2, 3],
                'overclocks': ['Eraser', 'Armor Break Module', 'Explosive Chemical Rounds', 'Seeker Rounds', 'Executioner', 'Neuro-Lasso'],
            },
        },
        'secondary': {
            'Deepcore 40mm PGL': {
                'tiers': [3, 2, 3, 3, 3],
                'overclocks': ['Clean Sweep', 'Pack Rat', 'Compact Rounds', 'RJ250 Compound', 'Fat Boy', 'Hyper Propellant'],
            },
            'Breach Cutter': {
                'tiers': [2, 3, 2, 2, 3],
                'overclocks': ['Light-Weight Cases', 'Roll Control', 'Stronger Plasma Current', 'Return to Sender', 'High Voltage Crossover', 'Spinning Death', 'Inferno'],
            },
            'Shard Diffractor': {
                'tiers': [3, 2, 2, 2, 3],
                'overclocks': ['Efficiency Tweaks', 'Automated Beam Controller', 'Feedback Loop', 'Volatile Impact Reactor', 'Plastcrete Catalyst', 'Overdrive Booster'],
            },
        },
        'equipment': [
            {
                'name': 'Platform Gun',
                'tiers': [3, 1, 3],
            },
            {
                'name': 'LMG Gun Platform',
                'tiers': [2, 3, 3, 2],
            },
        ],
        'armor': [3, 2, 1, 3],
        'throwables': ['L.U.R.E.', 'Plasma Burster', 'Proximity Mine'],
    },
    'gunner': {
        'primary': {
            '"Lead Storm" Powered Minigun': {
                'tiers': [3, 2, 3, 3, 3],
                'overclocks': ['A Little More Oomph!', 'Thinned Drum Walls', 'Burning Hell', 'Compact Feed Mechanism', 'Exhaust Vectoring', 'Bullet Hell', 'Lead Storm'],
            },
            '"Thunderhead" Heavy Autocannon': {
                'tiers': [3, 3, 3, 2, 3],
                'overclocks': ['Composite Drums', 'Splintering Shells', 'Carpet Bomber', 'Combat Mobility', 'Big Bertha', 'Neurotoxin Payload'],
            },
            '"Hurricane" Guided Rocket System': {
                'tiers': [3, 2, 2, 2, 3],
                'overclocks': ['Manual Guidance Cutoff', 'Overtuned Feed Mechanism', 'Fragmentation Missiles', 'Plasma Burster Missiles', 'Minelayer System', 'Jet Fuel Homebrew', 'Salvo Module'],
            },
        },
        'secondary': {
            '"Bulldog" Heavy Revolver': {
                'tiers': [2, 3, 3, 2, 2],
                'overclocks': ['Chain Hit', 'Homebrew Powder', 'Volatile Bullets', 'Six Shooter', 'Elephant Rounds', 'Magic Bullets'],
            },
            'BRT7 Burst Fire Gun': {
                'tiers': [3, 3, 2, 3, 2],
                'overclocks': ['Composite Casings', 'Full Chamber Seal', 'Compact Mags', 'Experimental Rounds', 'Electro Minelets', 'Micro Flechettes', 'Lead Spray'],
            },
            'ArmsKore Coil Gun': {
                'tiers': [3, 3, 2, 2, 3],
                'overclocks': ['Re-atomizer', 'Ultra-Magnetic Coils', 'Backfeeding Module', 'The Mole', 'Hellfire', 'Triple-Tech Chambers'],
            },
        },
        'equipment': [
            {
                'name': 'Zipline Launcher',
                'tiers': [3, 1, 2],
            },
            {
                'name': 'Shield Generator',
                'tiers': [2, 2, 3],
            },
        ],
        'armor': [3, 2, 1, 3],
        'throwables': ['Sticky Grenade', 'Incendiary Grenade', 'Cluster Grenade'],
    },
    'scout': {
        'primary': {
            'Deepcore GK2': {
                'tiers': [2, 2, 3, 3, 3],
                'overclocks': ['Compact Ammo', 'Gas Rerouting', 'Homebrew Powder', 'Overclocked Firing Mechanism', 'Bullets of Mercy', 'AI Stability Engine', 'Electrifying Reload'],
            },
            'M1000 Classic': {
                'tiers': [2, 3, 2, 2, 3],
                'overclocks': ['Hoverclock', 'Minimal Clips', 'Active Stability System', 'Hipster', 'Electrocuting Focus Shots', 'Supercooling Chamber'],
            },
            'DRAK-25 Plasma Carbine': {
                'tiers': [3, 2, 3, 3, 2],
                'overclocks': ['Aggressive Venting', 'Thermal Liquid Coolant', 'Impact Deflection', 'Rewiring Mod', 'Overtuned Particle Accelerator', 'Shield Battery Booster', 'Thermal Exhaust Feedback'],
            },
        },
        'secondary': {
            'Jury-Rigged Boomstick': {
                'tiers': [2, 2, 3, 3, 3],
                'overclocks': ['Compact Shells', 'Double Barrel', 'Special Powder', 'Stuffed Shells', 'Shaped Shells', 'Jumbo Shells'],
            },
            'Zhukov NUK17': {
                'tiers': [2, 3, 2, 3, 2],
                'overclocks': ['Minimal Magazines', 'Custom Casings', 'Cryo Minelets', 'Embedded Detonators', 'Gas Recycling'],
            },
            'Nishanka Boltshark X-80': {
                'tiers': [3, 3, 2, 2, 3],
                'overclocks': ['Quick Fire', 'The Specialist', 'Cryo Bolt', 'Fire Bolt', 'Bodkin Points', 'Trifork Volley'],
            },
        },
        'equipment': [
            {
                'name': 'Grappling Hook',
                'tiers': [2, 1, 2, 3],
            },
            {
                'name': 'Flare Gun',
                'tiers': [2, 2, 3],
            },
        ],
        'armor': [3, 2, 1, 3],
        'throwables': ['Inhibitor-Field Generator', 'Cryo Grenade', 'Pheromone Canister'],
    },
}

pickaxe = [1, 3]

perks = {
    'active': [
        'Beast Master',
        'Berzerker',
        'Dash',
        'Field Medic',
        'Heightened Senses',
        'Hover Boots',
        'Iron Will',
        'See You In Hell',
        'Shield Link',
    ],
    'passive': [
        'Born Ready',
        'Deep Pockets',
        'Elemental Insulation',
        'Friendly',
        'It\'s a Bug Thing',
        'New Passive Perk Slot',
        'Resupplier',
        'Second Wind',
        'Strong Arm',
        'Sweet Tooth',
        'Thorns',
        'Unstoppable',
        'Vampire',
        'Veteran Depositor',
    ],
}
