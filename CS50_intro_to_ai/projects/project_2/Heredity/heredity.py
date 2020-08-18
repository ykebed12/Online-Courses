import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

# parent gene {}
# parenttrait {}
# child gene  {}
# child trait {}


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    GENE_PROB = 0.5    # Probability that the first gene is selected 
    
    data = {}
    for name, person_data in people.items():
        data[name] = person_data.copy()
        if name in two_genes:
            data[name]['gene'] = True, True
        elif name in one_gene:
            data[name]['gene'] = True, False
        else:
            data[name]['gene'] = False, False

        data[name]["have_trait"] = name in have_trait

    probability = 1

    for name in data:
        mother = data.get(data[name]["mother"])
        father = data.get(data[name]["father"])

        person = data[name]
        gene_num = sum(person['gene'])
        trait = person['have_trait']

        if father == None and mother == None:
            
            probability *= (PROBS['gene'][gene_num] *
                            PROBS['trait'][gene_num][trait])
        else:
            
            child_probability = 0

            for gene_comb in itertools.product(mother['gene'],
                                               father['gene']):
                
                if sum(gene_comb) == gene_num:

                    child_probability += (GENE_PROB * (1-GENE_PROB) *
                                          (1-PROBS["mutation"])**2)
                if sum((not gene_comb[0], gene_comb[1])) == gene_num:

                    child_probability += (GENE_PROB * (1-GENE_PROB) * 
                                          (1-PROBS["mutation"]) * 
                                          PROBS["mutation"])
                if sum((gene_comb[0], not gene_comb[1])) == gene_num:
                    
                    child_probability += (GENE_PROB * (1-GENE_PROB) * 
                                          (1-PROBS["mutation"]) * 
                                          PROBS["mutation"])
                if sum((not gene_comb[0], not gene_comb[1])) == gene_num:

                    child_probability += (GENE_PROB * (1-GENE_PROB) *
                                          PROBS["mutation"]**2)

            probability *= child_probability * PROBS['trait'][gene_num][trait]

    return probability

        

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for name, data in probabilities.items():
        if name in one_gene:
            data['gene'][1] += p
        elif name in two_genes:
            data['gene'][2] += p
        else:
            data['gene'][0] += p

        if name in have_trait:
            data['trait'][True] += p
        else:
            data['trait'][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for data in probabilities.values():
        gene_factor = 1 / sum(data['gene'].values())
        trait_factor = 1 / sum(data['trait'].values())
        for k_gene, v_gene in data['gene'].items():
            data['gene'][k_gene] = v_gene * gene_factor
        for k_trait, v_trait in data['trait'].items():
            data['trait'][k_trait] = v_trait * trait_factor
    


if __name__ == "__main__":
    main()
