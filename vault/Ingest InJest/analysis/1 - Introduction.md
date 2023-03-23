# Preface

Ingest In-Jest is a project intended to use David Foster Wallace's 1996 book "Infinite Jest" as a primary vehicle for working out an approach to systematic analysis of a complex work.  This is part data processing design, part programming, part literary theory, and part practical application of that theory.

Anything can be analyzed.  Everthing is data.  Early in my career, during a particuarly overworked time, I recall having a nightmare in which I was tabulating a plate of scrambled eggs.  I don't remember the details of my implementation, but I remember coming away from that with the sure knowledge that whatever I did...it had WORKED.  This principle applies now more than ever, as there are myriad tools that allow opportunities for messy things to be...un-messed, I guess.  Countable.  Semi-structured.  

# WTF is structure and how do we codify it
You can figure that everything you can think of has some notion of structure at least, even if it's just a set of equations that govern the unstructured chaotic motion of the particles in a puff of smoke or whatever...math and science is full of stuff like this.  So there's nothing that is *truly* un-structured, but there are plenty of phenomena in nature that don't quickly lend themselves to easy analysis.

The real trick of observation here is that you have to pick a viewpoint - a 'lens' to look through, which would include both the 'context' in which we are observing the thing, and the 'resolution' to which we want to focus. 

Consider that puff of smoke, and some science bitch that wants to analyze it.  So they set up some experiment in a lab where they blow smoke with a fan across a camera, and track how the whorls form and all that crap.  The lens in our abstract analogy is what we can see in the camera, and the resolution is sort of a combination of the camera speed and how small they can make the grid that overlays the space they can see...how many slices can they look at in a single frame.  Establish a timeline.  Watch how things unfold, and track them on a series of grids, one per time slice.  There's useful and analyzable data about a puff of smoke, ready to be put into a model.

We can pull that same trick with anything - people do all the time, that's what is going on in labs and practical field work always, everywhere.  It's not an aspect of it that we usually pay attention to, but the how-do-you-break-stuff-down thing is pretty much built in to any kind of analysis.  We can then think okay, well maybe how HARD is it to do that...with the smoke thing for instance, it's pretty much impossible to do that analysis without specialized equipment like the camera, computer, and general laboratory conditions...it would mean less in the park on a windy day, just trying to do it by eye.  So methodology is necessarily constrained by equipment, time, labor, and scope.  All of that is worth keeping in mind as we do this.

# Scope, Resolution, Lenses, Viewpoints, etc.

## A speculative story about a failure of resolution.
Think of a giant board of Conway's "Game of Life" - let's say a trillion cells along a side of the grid, and we're looking at a 1000x per second run, with a 4k video of the thing rolling, zoomed out so we can see the whole grid on the screen.  Could you derive the eight straightforward binary conditions that govern the simulation from that?  This is 4k video, so 3840x2160 - so each cell on the board is 1,000,000,000,000 / 2000 = give me a fucking break - we could never see the individual moves from there.  We'd have to zoom so far in, in order to see the individual actions, or indeed even the individual spots...we would only see vague gradients at that resolution.  We'd have to develop a new field of spectroscopy just for this game in order to even analyze that at all, and the notion of working back from that into the simple starting conditions is ludicrous. I think maybe it could only be verified by correctly deriving those conditions, then repeating the exact conditions of the randomized starting setup, and verifying that the exact same gradient takes place - which it would, because this is a simple deterministic system - but even just telling that it's the same gradient at this resolution would be dependent upon a number of hardware factors that we haven't even considered....because the problem is not now the system we're analyzing, but the tool - the 4k video encoder, the cpu, all of the things that might contribute to a single pixel being just a hair darker or lighter on one run vs another - undetectable to the naked eye, and unnoticeable until you're looking to find an exact match .... how do you ever call something like this truly verified.  Even if you had it exactly right, you'd never goddamn know.

If you had a zoom, and you could zoom to a factor of ten billion, we're now looking at a piece that is ten million along a side, and if we slice that into 2000 piece we are now looking at 500 grid cells per pixel, roughly. That's still not nearly enough to see the cells doing their thing, but you could see a much better gradient at this level - one which, in a world where you have correctly derived both the rules and the starting position, and re-run the simulation, doing statistical analysis to see that the same pattern appears over and over again - that this could be considered sort of in the land of verification.

Push your technology a little farther, and zoom in another 1000x, and you've got everything you need to be 'sure'...you'd be able to see the individual cells in your video, and ohhhhhh....yeah we'd have to make sure it's a high speed camera all this time, because at 1k iterations per second, we'll need to break it into that precise number of video frames per second, lined up to when the iterations flip.  That could get a little complicated, but I guess it's technically doable.  

So...equipment.  Assumptions.  Viewpoint.  Scope.  Labor.  Don't know what the point of that exactly is, but it seems like it's probably important.

# This is about a book, asshole.  How does this apply to books.
A book, or natural text in general, is SEMI-structured, because although it's not generally arranged into some numbered grid for us that is full of useful contextual information or something, we can say that the very granular pieces of it - letters/symbols - are already 'known' things from the standpoint of representation.  There are a finite number of grains that matter, and the computer already knows what they are and a ton of basics about how they work, and there are a lot of tools that work on them.  There's tons of methods for transferring non-digital text to digital, but anything that's already 'in the computer' is at a baseline that can be used right out of the box.  We have that, in this case and in many others.  The trick then is in not in the 'substrate' so to speak - those are just text files or whatever, but in the combinations of the symbols - from the get-go, there's an infinite way of putting together all these little pieces that we have easy access to.

So some combinations of these things are more 'important' - one of the most basic of these aggregated structures are things we could call 'words'.  They mainly serve as buckets of meaning - each one generally has a list of things that it can mean in different contexts.  People have done a lot of work in this area, and continue to - that shit is called dictionaries.  For our purposes, approaching this from a programming standpoint, this is another home run - we have easy, publically available, programmatic access to the property list of our second-level granules.  So far so good.

Another level up we can say that we have combinations of words, which we typically call 'phrases', further classified into 'sentences'.  These are even more constrained in terms of the valid word combinations, so the infinity we started with is a LOT smaller by now.  

But hang on - DO they have to be 'right', or constrained at all?  This is reality, and it's messy.  So no, it turns out that baseball hieroglyphics hopscotch pouch, after all...but in data analysis we can also cheat and say that 'exceptions' is a bucket unto itself.  Just because some tool that some guy built (a dictionary, a grammar, etc) works on most things, doesn't mean it's the only tool.  

That's what this project is about in the first place...we have to build our own.  So it's this level - really the previous level, because words don't have to wrtbwrp either - upon which we must begin our setup.  

# Lexicon, Onotology, Taxonomy
[[Casting LOTs]], we might call it - I just thought of that as I typed it, and I've unilaterally decided that's what this will be called from now on - refers to the practice of building up a [[tangled hierarchy]] of 'meaning' from the basic pieces (letters) up through what we might think of as a list of 'notions'.  The three levels represent the words themselves ([[lexicon]]), the basic set of things that can be represented ([[ontology]]) and the bucket-system that those things exist in, for purposes of our work ([[taxonomy]]).  Bear in mind that the result is NOT the sort of cladistic structure that you might think of when you hear 'taxonomy', but a looser structure where things can connect in a multitude of directions.

This will be one of the major tasks of this whole thing, maybe really the trunk of it, if there is one.  This is where all that crap about the smoke and the grids comes into play - this structure that we'll make is *how* we will establish what our resolution is, and how we can view it from different angles.

Practically, think of it like a bunch of different kinds of lists, and each one of those lists has a bunch of tags - almost like basically hashtags, like you would think of them.  We'll primarily use spreadsheets and such to do this part of the work, which will exist in this sort of loop where the computer does part of the work and the Human Operators, or 'HO's, as I like to call them, do part of the work. 

# Narrative vs ...not...Narrative, I guess
There's lots of types of writing, and most of them are not narrative.  Technical writing, opinion pieces, ad copy, magazine articles, blogs, tweets, posts, bludds, wastoids, dweebies, dickheads...we're not really worried about those things in this.  I mean - well, really, any of those things could be thrown into the same kind of system, so don't think I'm dismissing the idea...it's more that the most complex and therefore interesting of these are narratives, if only because the narrative form necessarily has a through-line (it says all of the things it's going to say), and that through-line can be mapped to an 'actual' history that the narrative purports to relate, or comment upon.  The model as I have it in mind is most robust when these things exist in a meaningful relationship.

How can we picture this.  Okay, we're going to make a Beautiful Mind/Pepe Silvia/police-procedural thing on the wall, and we're going to use two threads, a blue one and a green one.  The blue one represents the story, and the gree-n one represents the world - at least the world where the story takes place.  In fact let's add a third thread, a brown one, which represents our real world.

# Narrative levels
- Corpus
- Volume
- Chapter
- Scene
- Paragraph
- Sentence OR [[Fragment]]
- Phrases
- Words
- Symbols

# Timelines
## Narrative
- requires a POV, at more than one level (author > narrator > character)
- can skip around
- can contradict
- can falsify
- 100% of the narrative is present in the work

## History
- 'objective', technically unfalsifiable
- doesn't skip around
- contradictions can be recorded, but not resolved
- mostly unknown
- POVs might be the 'real' world and the world(s) of the narrative


