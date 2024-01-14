import string
import random


def generatingName():
    firstName = [
        "Adam", "Adrian", "Alan", "Albert", "Alex", "Alexander", "Alfred", "Alice", "Alicia", "Alison",
        "Amelia", "Amy", "Andrew", "Andy", "Angela", "Anna", "Anne", "Annie", "Anthony", "Anton", "Arthur",
        "Ashley", "Barbara", "Beatrice", "Ben", "Benjamin", "Bernard", "Beth", "Betsy", "Betty", "Bill",
        "Billy", "Bob", "Brad", "Bradley", "Brandon", "Brenda", "Brian", "Brianna", "Bruce", "Cameron",
        "Carl", "Carlos", "Carmen", "Carol", "Caroline", "Carrie", "Catherine", "Charles", "Charlotte",
        "Cheryl", "Chris", "Christian", "Christina", "Christine", "Christopher", "Clara", "Clarence",
        "Claude", "Claudia", "Clifford", "Clint", "Cynthia", "Dale", "Daniel", "Danielle", "Danny", "David",
        "Deborah", "Denise", "Dennis", "Diana", "Diane", "Donald", "Donna", "Dorothy", "Douglas", "Dylan",
        "Edith", "Edward", "Eleanor", "Elizabeth", "Emily", "Emma", "Eric", "Erik", "Erin", "Eugene",
        "Eva", "Evelyn", "Faye", "Felicia", "Florence", "Frances", "Francis", "Frank", "Fred", "Gabriel",
        "Gary", "George", "Gerald", "Gina", "Glenn", "Gloria", "Grace", "Greg", "Gregory", "Hannah",
        "Harold", "Harry", "Heather", "Helen", "Henry", "Howard", "Ian", "Isaac", "Jack", "Jacob", "James",
        "Jane", "Janet", "Janice", "Jason", "Jean", "Jeff", "Jeffrey", "Jennifer", "Jerry", "Jessica", "Jim",
        "Jimmy", "Joan", "Joe", "John", "Johnny", "Jonathan", "Jordan", "Joseph", "Joshua", "Joyce", "Juan",
        "Judith", "Judy", "Julia", "Julian", "Julie", "Justin", "Karen", "Katherine", "Kathleen", "Kathy",
        "Katie", "Keith", "Kelly", "Kenneth", "Kevin", "Kim", "Kyle", "Larry", "Laura", "Lauren", "Lawrence",
        "Lena", "Leo", "Leonard", "Lillian", "Linda", "Lisa", "Lloyd", "Lois", "Loretta", "Louis", "Louise",
        "Lucas", "Lucille", "Lucy", "Luke", "Luther", "Lynn", "Mabel", "Mae", "Marc", "Margaret", "Maria",
        "Marian", "Marie", "Marilyn", "Mario", "Marion", "Mark", "Martha", "Martin", "Mary", "Matthew",
        "Maureen", "Max", "Megan", "Melanie", "Melissa", "Michael", "Michelle", "Mildred", "Milton", "Mona",
        "Monica", "Nancy", "Natalie", "Nathan", "Nathaniel", "Neil", "Nicholas", "Nicole", "Nina", "Norma",
        "Olivia", "Oscar", "Pamela", "Patricia", "Patrick", "Paul", "Paula", "Peggy", "Peter", "Philip",
        "Phillip", "Phyllis", "Rachel", "Ray", "Raymond", "Rebecca", "Regina", "Renee", "Rhonda", "Richard",
        "Rick", "Rita", "Robert", "Roberta", "Robin", "Roger", "Ronald", "Rosalie", "Rose", "Roy", "Ruby",
        "Russell", "Ruth", "Ryan", "Samantha", "Samuel", "Sandra", "Sara", "Sarah", "Scott", "Sean", "Sharon",
        "Shawn", "Sheila", "Shirley", "Sidney", "Stacy", "Stanley", "Stephen", "Steve", "Steven", "Susan",
        "Sylvia", "Tammy", "Teresa", "Terry", "Theodore", "Thomas", "Timothy", "Tina", "Tom", "Tony", "Tracy",
        "Tyler", "Vanessa", "Veronica", "Vicki", "Vicky", "Victoria", "Vincent", "Virginia", "Walter", "Warren",
        "Wayne", "Wendy", "Willard", "William", "Willie", "Winston", "Yvonne", "Zachary", "Zoe",
        "Aidan", "Aiden", "Aileen", "Alanis", "Alberta", "Albina", "Aleah", "Alessia", "Alexandria", "Alice",
        "Alina", "Aliza", "Amalia", "Amaris", "Amaya", "Anahi", "Anaya", "Angela", "Angelica", "Anya", "April",
        "Aria", "Ariana", "Ariella", "Arya", "Ashlyn", "Athena", "Audrina", "Aurelia", "Aurora", "Ayla", "Azalea",
        "Belen", "Bethany", "Blakely", "Braelynn", "Briana", "Briella", "Brynn", "Caitlyn", "Cali", "Camilla",
        "Carmen", "Carolina", "Cassandra", "Cataleya", "Charlee", "Charlotte", "Cherish", "Christina", "Ciara",
        "Clarissa", "Clementine", "Colette", "Cynthia", "Dahlia", "Daisy", "Dalia", "Danica", "Daniella", "Danna",
        "Delaney", "Demi", "Desiree", "Destiny", "Dulce", "Edith", "Eileen", "Elena", "Elisa", "Eliza", "Eloise",
        "Elsa", "Elvira", "Ember", "Emerie", "Emery", "Emilia", "Emmaline", "Emmeline", "Esmeralda", "Estella",
        "Esther", "Evangeline", "Evelina", "Everleigh", "Fernanda", "Fiona", "Francesca", "Gabriela", "Genevieve",
        "Georgia", "Giovanna", "Giselle", "Grace", "Gwendolyn", "Hadley", "Haley", "Harmony", "Haven", "Hazel",
        "Heavenly", "Holly", "Hope", "Imani", "Ingrid", "Ireland", "Isabela", "Isabella", "Isis", "Ivory", "Ivy",
        "Jada", "Jade", "Jasmine", "Jenna", "Jessica", "Jocelyn", "Josephine", "Juliana", "Juliet", "June",
        "Juniper", "Kadence", "Kaitlyn", "Kara", "Karina", "Karla", "Katalina", "Kate", "Katherine", "Kendra",
        "Kenley", "Kimber", "Kinsley", "Kira", "Kirsten", "Kristina", "Laney", "Larissa", "Laura", "Lauren",
        "Layla", "Leah", "Leilani", "Lena", "Liana", "Liliana", "Lillian", "Lily", "Lorelei", "Lucia", "Luciana",
        "Luna", "Lydia", "Lyric", "Mabel", "Mackenzie", "Madalyn", "Madeleine", "Malia", "Mallory", "Margaret",
        "Mariah", "Marina", "Marissa", "Maya", "Mckenna", "Meadow", "Megan", "Melody", "Mercedes", "Mia",
        "Michaela", "Mila", "Miranda", "Miriam", "Monique", "Morgan", "Nadia", "Nala", "Naomi", "Natalia", "Nina",
        "Noelle", "Nora", "Nova", "Olivia", "Ophelia", "Paige", "Paisley", "Paloma", "Penelope", "Perla",
        "Phoenix", "Piper", "Poppy", "Presley", "Quinn", "Raven", "Rebecca", "Regina", "Riley", "Rosalie", "Rose",
        "Ruby", "Sabrina", "Sadie", "Sage", "Samara", "Samantha", "Savannah", "Scarlett", "Selena", "Serena",
        "Sienna", "Skylar", "Sophia", "Stella", "Summer", "Sunny", "Sydney", "Talia", "Tatiana", "Taylor",
        "Tiana", "Trinity", "Valeria", "Vera", "Veronica", "Victoria", "Vienna", "Violet", "Vivian", "Waverly",
        "Willow", "Ximena", "Yara", "Yasmine", "Zara", "Zariah", "Zoey"
    ]

    surName = ["Smith", "Müller", "Rossi", "Garcia", "Johnson", "Schneider", "Novak", "Martinez", "Andersen", "Petrov",
               "Nielsen", "Lopez", "Ivanov", "Fernandez", "Johnson", "Schneider", "Novak", "Martinez", "Andersen",
               "Petrov", "Nielsen", "Lopez", "Ivanov", "Fernandez", "Smith", "Müller", "Rossi", "Garcia", "Johnson",
               "Schneider", "Novak", "Martinez", "Andersen", "Petrov", "Nielsen", "Lopez", "Ivanov", "Fernandez",
               "Smith",
               "Rossi", "Garcia", "Johnson", "Schneider", "Novak", "Martinez", "Andersen", "Petrov", "Nielsen", "Lopez",
               "Ivanov", "Fernandez", "Smith", "Müller", "Rossi", "Garcia", "Johnson", "Schneider", "Novak", "Martinez",
               "Andersen", "Petrov", "Nielsen", "Lopez", "Ivanov", "Fernandez", "Smith", "Müller", "Rossi", "Garcia",
               "Johnson", "Schneider", "Novak", "Martinez", "Andersen", "Petrov", "Nielsen", "Lopez", "Ivanov",
               "Müller",
               "Fernandez", "Smith", "Müller", "Rossi", "Garcia", "Johnson", "Schneider", "Novak", "Martinez",
               "Andersen",
               "Petrov", "Nielsen", "Lopez", "Ivanov", "Fernandez"]

    return ''.join(random.choice(firstName) + ' ' + random.choice(surName))


def username(size=13, chars=None):
    if chars is None:
        chars = string.ascii_lowercase + random.choice(['.', '_'])
    word_list = [
        "Agatha", "Agnes", "Aileen", "Alice", "Amy", "Angela", "Beatrice", "Bridget", "Catherine",
        "Cordelia", "Dorothy", "Edith", "Elizabethe", "Emery", "Emma", "Esther", "Florence", "Frances",
        "Gertrude", "Helen", "Irene", "Issabel", "Judith", "Lucy", "Margaret", "Martha",
        "Mary", "Matilda", "Naomi", "Phyllis", "Rebecca", "Rosemary", "Sabina", "Silvester", "Sophia",
        "Winifred", "Abel", "Ace", "Ada", "Adam", "Adela", "Adelio", "Adolph", "Adonis", "Adora",
        "Agatha", "Aggie", "Aida", "Ailish", "Aimee", "Alan", "Albert", "Albino", "Alex",
        "Alexandra", "Alfred", "Ali", "Alice", "Alika", "Allie", "Aloha", "Alvin", "Amanda",
        "Ami", "Amos", "Amy", "Anais", "Andra", "Andrew", "Andy", "Angel", "Angelica", "Anika",
        "Anna", "Annie", "Anthony", "Apollo", "Aria", "Ariel", "Arista", "Arnold",
        "Arvid", "Asha", "Aster", "Astin", "Aurora", "Ava", "Baba", "Bailey", "Baldy",
        "Bambi", "Barbara", "Barbie", "Barley", "Barney", "Baron", "Basil", "Baxter", "Beau",
        "Bebe", "Beck", "Becky", "Belita", "Bella", "Belle", "Benecia", "Benny", "Berg", "Bessie",
        "Biana", "Bianca", "Bibiane", "Billy", "Bingo", "Bishop", "Bliss", "Blondie", "Bonita", "Bono",
        "Boris", "Boss", "Bright", "Bruno", "Buck", "Buddy", "Bunny", "Caesar", "Caley", "Calix",
        "Calla", "Callia", "Camilla", "Captain", "Cara", "Carmel", "Carmen", "Casey", "Catherine",
        "Cecil", "Celestyn", "Celina", "Cha Cha", "Champ", "Charles", "Charlie", "Chase", "Chavi",
        "Chelsea", "Cherie", "Chilli", "Chloe", "Chrissy", "Chubby", "Cindy", "Clara", "Clark",
        "Claudia", "Cleo", "Cleta", "Cliff", "Coco", "Cody", "Colin", "Connie", "coo", "Corby",
        "Coy", "Coyote", "Crimson", "Crispin", "Crystal", "Cutie", "Cyclone", "Cyma", "Daisy",
        "Dali", "Danika", "Darby", "Daria", "Darin", "Dario", "Darwin", "Dave", "David", "Dean",
        "Della", "Delling", "Delphine", "Dennis", "Denver", "Derry", "Deva", "Dexter", "Diallo",
        "Dick", "Dino", "Dixie", "Donna", "Doris", "Dorothy", "Douglas", "Duke", "Dustin", "Dyllis",
        "Eavan", "Ebony", "Echo", "Edan", "Edeline", "Eden", "Edward", "Edwin", "Eilis", "Eldora",
        "Elf", "Elin", "Elisha", "Elizabeth", "Elle", "Elroy", "Elsa", "Elvis", "Elysia", "Emilie",
        "Eric", "Eris", "Eros", "Esteban", "Esther", "Eva", "Evan", "Eve", "Farrell", "Favian",
        "Fedora", "Felice", "Felix", "Fella", "Fidelio", "Filia", "Fleta", "Florence", "Floria",
        "Forrest", "Freeman", "Gabriel", "Gali", "Gem", "Gemma", "George", "Gilbert", "Gili",
        "Giovanni", "Gloria", "Goofy", "Grace", "Grania", "Gregory", "Haley", "Halona", "Happy",
        "Harley", "Harmony", "Harold", "Harry", "Heba", "Helen", "Helia", "Hera", "Hero", "Hestia",
        "Hollis", "Honey", "Hope", "Hubert", "Hue", "Huey", "Ian", "Iliana", "Indira", "Ingrid",
        "Irina", "Iris", "Isaac", "Isabel", "Isadora", "Isis", "Jace", "Jack", "Jackson", "Jaclyn",
        "Jade", "Jane", "Jasmine", "Jasper", "Jefferson", "Jeffrey", "Jenifer", "Jennie", "Jeremy",
        "Jericho", "Jerry", "Jess", "Jessica", "Jessie", "Jodie", "Johanna", "Jolly", "Jordan", "Joy",
        "Jud", "Julia", "Juliana", "Juliet", "Justin", "Kali", "Kara", "Karena", "Karis", "Kassia",
        "Kate", "Kellan", "Kelley", "Kerri", "Kevin", "Kitty", "Klaus", "Kori", "Kuper", "Kyra",
        "Lakia", "Lala", "Lamis", "Lani", "Lappy", "Lara", "Lavina", "Lee", "Leena", "Lelia", "Leo", 'Love'
                                                                                                     "Leopold", "Lev",
        "Lidia", "Lily", "Lina", "Linda", "Lisa", "Lloyd", "Lonnie", "Lottie", "Louis",
        "Lowell", "Lucia", "Lucifer", "Lucy", "Lukas", "Luna", "Mabel", "Madonna", "Maggie", "Makaio",
        "Malissa", "Malo", "Mana", "Mandelina", "Manon", "Marcia", "Margaret", "Mary", "Mathilda",
        "Maya", "Melina", "Meriel", "Mickey", "Mighty", "Minnie", "Miranda", "Missy", "Misty", "Molly",
        "Monet", "Monica", "Morris", "Muffin", "Mulan", "Murphy", "Nadia", "Nalo", "Nami", "Nana",
        "Nani", "Naomi", "Nara", "Narcisse", "Navid", "Neal", "Neema", "Nero", "Nia", "Nicholas",
        "Nicky", "Nina", "Odelia", "Olga", "Olive", "Oliver", "Oscar", "Pablo", "Paloma", "Pamela",
        "Patrick", "Pavel", "Peggy", "Pello", "Penda", "Peppi", "Petra", "Phila", "Phillip", "Pinky",
        "Pluto", "Poco", "Polo", "Pooky", "Poppy", "Primo", "Prince", "Princess", "Puffy", "Rabia",
        "Raina", "Ralph", "Rambo", "Rania", "Ravi", "Redford", "Reggie", "Rei", "Remy", "Rex", "Richard",
        "Ricky", "Ringo", "Rio", "Risa", "Robbie", "Robert", "Robin", "Rocky", "Roja", "Rollo", "Romeo",
        "Rosie", "Roxy", "Roy", "Ruby", "Rudolph", "Rudy", "Ryan", "Sabrina", "Sally", "Salvatore",
        "Sam", "Samson", "Sandy", "Sarah", "Sasha", "Scarlet", "Scoop", "Sebastian", "Selina", "Selma",
        "Serena", "Severino", "Shaina", "Shasa", "Sheri", "Silky", "Simba", "Simon", "Sniper", "Solomon",
        "Sonia", "Sonny", "Sophie", "Sora", "Sparky", "Spooky", "Spotty", "Stella", "Steven", "Sting",
        "Storm", "Sugar", "Sunny", "Sweetie", "Sylvester", "Sylvia", "Talia", "Talli", "Tanesia",
        "Tania", "Ted", "Teenie", "Terra", "Tess", "Thomas", "Tomo", "Trisha", "Trudy", "Uba",
        "Umberto", "Valencia", "Vanessa", "Velika", "Vera", "Verdi", "Veronica", "Victoria",
        "Vincent", "Violet", "Vito", "Vivi", "Waldo", "Walter", "Weenie", "Wendy", "William",
        "Wily", "Winston", "Woody", "Yaro", "Yeti", "Yuki", "Zaza", "Zeki", "Zelia", "Zena",
        "Zenia", "Zenon", "Zeppelin", "Zeus", "Zili", "Zinna", "Zizi", "Zoe", "Zorro", "Zulu",
    ] + list(chars)

    result_username = 'x' * 100

    while not (size <= len(result_username) < 17):
        target_word_list = [
            (
                word[::-1] if random.random() < 0.05 else
                ''.join(
                    random.choice(['x', 'y'] + list(map(str, range(10)))) if random.random() < 0.03 else ch
                    for ch in word
                ) if random.random() < 0.03 else
                word + (word[-1] * random.randint(1, 4)) if random.random() < 0.07 else
                word
            ).lower() for word in random.choices(word_list, k=random.randint(1, 2))
        ]

        joining_char = random.choice(['.', '_'])
        additional_numbers = ''.join(random.choices(string.digits, k=random.randint(1, 6)))

        result_username = joining_char.join(target_word_list) + (joining_char + additional_numbers if random.random() < 0.3 else '')

    return result_username


def generatePassword(passwd=None):
    if passwd is None:
        password_characters = string.ascii_letters + string.digits
        return ''.join(random.choice(password_characters) for i in range(10))
    else:
        return passwd
