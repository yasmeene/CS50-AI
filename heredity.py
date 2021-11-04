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

    joint = 1
    # iterating through the people dictionary 
    for person in people:
        
        personP = 1
        # defines the mother and father of the family
        motherP = people[person]['mother']
        fatherP = people[person]['father']

        # checks to see which genes a person has and adds it to person_genes
        if person in two_genes:
            person_genes = 2
        elif person in one_gene:
            person_genes = 1
        else:
            person_genes = 0
        
        if person in have_trait:
            person_trait = True
        else: 
            person_trait = False
        
        # if person has no parents listed, we use the idependent prob
        if not motherP and not fatherP:
            personP *= PROBS["gene"][person_genes]
        
        # checks if parents are listed
        else:
            # if mother is in one_gene then they will pass the gene with a 50% prob to their child
            if motherP in one_gene:
                m_gene_per = 0.5

            # if they are in two_genes, then they will pass one of the genes to their child
            elif motherP in two_genes:
                m_gene_per = 1 - PROBS['mutation']
            
            # else the only way the mother can pass a gene is if it mutates
            else:
                m_gene_per = PROBS['mutation']
            
            
            if fatherP in one_gene:
                f_gene_per = 0.5

            elif fatherP in two_genes:
                f_gene_per = 1 - PROBS['mutation']
            
            else:
                f_gene_per = PROBS['mutation']

            # finding an individuals probability of having a gene given their parents genes
            if person_genes == 2:
                personP *= m_gene_per * f_gene_per

            elif person_genes == 1:
                personP *= (1 - m_gene_per) * f_gene_per + (1 - f_gene_per) * m_gene_per

            else:
                personP = (1 - m_gene_per) *  (1 - f_gene_per)

        
        personP *= PROBS['trait'][person_genes][person_trait]
        joint *= personP

    return joint


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    # iterates through people in prob dict
    for person in probabilities:

        # checks if they have respective num of genes/ no genes
        if person in one_gene:
            gene_num = 1
        elif person in two_genes:
            gene_num = 2
        else:
            gene_num = 0
        
        # adds joint prob to prob dict
        probabilities[person]["gene"][gene_num] += p

        if person in have_trait:
            trait_val = True
        else:
            trait_val = False

        probabilities[person]["trait"][trait_val] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    # iterate through probabilities 
    for person in probabilities:

        # sum all values in gene and trait set
        genes_sum = sum(probabilities[person]['gene'].values())
        traits_sum = sum(probabilities[person]['trait'].values())


        # for all 3 gene values, divide gene value by gene sum
        for i in range(0,3):
            probabilities[person]['gene'][i] /= genes_sum
        
        # for both trait booleans, divide trait bool by trait sum
        for i in range(0,2):
            probabilities[person]['trait'][i] /= traits_sum


if __name__ == "__main__":
    main()
