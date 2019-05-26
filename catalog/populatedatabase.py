from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Genre, Movies, Base

engine = create_engine('sqlite:///moviegenre.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create a horror genre.
horror = Genre(name="Horror")
session.add(horror)
session.commit()

#Horror movie one.
movie_description = """In 1970, paranormal investirgators and demonlogists Lorriance and Ed
                       Warren are summored to the home of Carolyn and Roger Perron. The Perrons
                       and their five daugthers have recently moved into a srcluded farmhouse, 
                       where a supernatural presence has made iteself known. Though the manifestation
                       are benign at first, they soon escalate in horrifying fashion."""
                       # description taken from google revie and description - search for The conjuring.
conjuring = Movies(name="The Conjuring",
                   description=movie_description,
                   year=2013,
                   genre=horror)
session.add(conjuring)
session.commit()

# Horror movie two.
# Description taken from google reviews and description - search for The nightmare on elm street 1984.
movie_description_2 = """In Wes Cravens's Classic Slasher film, several teenagers fall prey to Freddy Krueger,
                         a disfigured midnight mangler who preys on the teenagers in their dreams - which in turn,
                         kills them in reality. After investigating the phenomenon, Nancy begins to suspect that 
                         a dark secret kept by her and her friend's parents may be the key to solve the mystery. """
nightmare = Movies(name="The Nightmare on Elm Street",
                   description=movie_description_2,
                   year=1984,
                   genre=horror)
session.add(nightmare)
session.commit()

# Horror movie three.
# Description taken from google review and descriptions - search for "The Texas Chain Saw Massacre 2003." IMDB.
movie_description_3 = """After picking up a traumatized young hitchhiker, five friends find themselves stalked and hunted
                         by a deformed chainsaw-wielding loon and hist family of equally psychopathic killers."""
massacre = Movies(name="The Texas Chainsaw Massacre",
                  description=movie_description_3,
                  year=2003,
                  genre=horror)
session.add(massacre)
session.commit()

###########################################################
# Create action genre.
action = Genre(name="Action")
session.add(action)
session.commit()


# These are from: www.imdb.com/list/ls027328830
# Action Movie one:
action_description_1 = """In a future where mutants are nearly extinct, an elderly and weary
                          Logan leads a quite life. But when Laura, a mutant child pursued by 
                          scientists, comes to him for help, he must get her to safety."""
logan = Movies(name="Logan",
               description=action_description_1,
               year=2017,
               genre=action)
session.add(logan)
session.commit()

# Action movie 2: 
action_description_2 = """After the devastating events of Avengers: infinity war, the universe is in ruins.
                          with the help of remaning allies, the Avengers assemble once more in order to undo
                          Thanos' actions and restore order to the universe. """
endgame = Movies(name="Avengers: Endgame",
                 description=action_description_2,
                 year=2019,
                 genre=action)
session.add(endgame)
session.commit()

# Action movie 3:
action_description_3 = """An ex-hit-man comes out of retirement to track down
                          the gangsters that killed his dog and took everything
                          from him."""
wick = Movies(name="John Wick",
              description=action_description_3,
              year=2014,
              genre=action)
session.add(wick)
session.commit()


###########################################################
# Create Thriller Genre.
thriller = Genre(name="Thriller")
session.add(thriller)
session.commit()

# Movies from https://www.imdb.com/search/title?genres=thriller&groups=top_250&sort=user_rating,desc&ref_=adv_prv
# Thriller movie 1: 
thriller_description_1 = """When the Menace known as the Joker emerges from his mysterious past, he wreaks
                            havoc and chaos on the people of Gotham. The Dark Knight must accept one of the greates pyschological
                            and physical tests of this ability to fight injustice. """
dark_knight = Movies(name="The Dark Knight",
                     description=thriller_description_1,
                     year=2008,
                     genre=thriller)
session.add(dark_knight)
session.commit()

# Thriller movie 2: 
thriller_description_2 = """A thief steals corporate secrets through the use of dream-sharing technology
                            is given the invers task of planting an idea into a mind of a CEO."""
inception = Movies(name="Inception",
                   description=thriller_description_2,
                   year=2010,
                   genre=thriller)
session.add(inception)
session.commit()
 
# Thriller movie 3: 
thriller_description_3 = """A Young FBI Candet must recieve the help of an incarcerated and manipulated
                            cannibal killer to help catch another serial killer, a madman who skins his victims."""
silence_of_the_lamb = Movies(name="Slience of the Lamb",
                             description=thriller_description_3,
                             year=1991,
                             genre=thriller)
session.add(silence_of_the_lamb)
session.commit()

###########################################################
# Creating Classic Genre.
classic = Genre(name="Classic")
session.add(classic)
session.commit()

# These movies are from: https://www.imdb.com/list/ls000183548/
# Classic movie 1: 
classic_description = """A manipulative woman and a roguish man conduct a turbulent romance during the American Civil War and Reconstruction periods."""
gone_with_the_wind = Movies(name="Gone with the Wind.",
                            description=classic_description,
                            year=1939,
                            genre=classic)
session.add(gone_with_the_wind)
session.commit()


# CLassic movie 2: 
classic_description_2 = """Dorothy Gale is swept away from a farm in Kansas to a magical land of Oz 
                           in a tornado and embarks on a quest with her new friends to see the Wizard 
                           who can help her return home to Kansas and help her friends as well. """
oz = Movies(name="The Wizard of Oz",
            description=classic_description_2,
            year=1939,
            genre=classic)

# adding the movie in
session.add(oz)
session.commit()

# Classic movie 3: 
classic_description_3 = """The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son. """
god_father = Movies(name="The Godfather",
                    description=classic_description_3,
                    year=1972,
                    genre=classic)
# adding movie.
session.add(god_father)
session.commit()


###########################################################
# Creating Comedy Genre.
comedy = Genre(name="Comedy")
session.add(comedy)
session.commit()

# Getting this movies from: https://www.imdb.com/search/title?genres=comedy&groups=top_250&sort=user_rating&title_type=feature
# comedy movie 1: 
comedy_description_1 = """ Marty McFly, a 17-year-old high school student,
                           is accidentally sent thirty years into the past in a time-traveling DeLorean invented
                           by his close friend, the maverick scientist Doc Brown."""
back_to_the_future = Movies(name="Back to the Future",
                            description=comedy_description_1,
                            year=1985,
                            genre=comedy)
# adding movie.
session.add(back_to_the_future)
session.commit()

# comedy movie 2: 
comedy_description_2 = """A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy's room."""
toy_story = Movies(name="Toy Story",
                   description=comedy_description_2,
                   year=1995,
                   genre=comedy)
# adding movie
session.add(toy_story)
session.commit()

# comedy movie 3: 
comedy_description_3 = """King Arthur and his Knights of the Round Table embark on a surreal,
                          low-budget search for the Holy Grail, encountering many, very silly obstacles."""
monty_python = Movies(name="Monty Python and the Holy Grail",
                      description=comedy_description_3,
                      year=1975,
                      genre=comedy)

# adding movie.
session.add(monty_python)
session.commit()


###########################################################
# Creating Drama Genre.
drama = Genre(name="Drama")
session.add(drama)
session.commit()

# These movies are from: https://www.imdb.com/list/ls009668711/
# Drama movies 1
drama_description = """The lives of two mob hitmen, a boxer, a gangster & his wife, and a pair of diner bandits intertwine in four tales of violence and redemption."""
pulp_fiction = Movies(name="Pulp Fiction",
description=drama_description,
year=1994,
genre=drama)

# adding movie
session.add(pulp_fiction)
session.commit()

# Drama movie 2
drama_description_2 = """A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery."""
gladiator = Movies(name="Gladiator",
description=drama_description_2,
year=2000,
genre=drama)

#adding movie
session.add(gladiator)
session.commit()

# Drama movie 3
drama_description_3 = """A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic."""
titanic = Movies(name="Titanic",
description=drama_description_3,
year=1997,
genre=drama)

#adding movie
session.add(titanic)
session.commit()

print engine
print "finished populating a database."

