cheshirenet
===========

The nework without a medium is like a smile without a cat

What is this thing all about
----------------------------

Have you noticed than revolution made by Tim Berners-Lee have  somehow reversed revolution made by Gutenberg?
In the world of printed books each text exists in thousand copies, and no one is able to silence a word, once word have been printed and copies sold. Even most oppressive goverments were unable to collect and burn all the copies of most hated books.

Moreover, in the pre-Web world everyone kept a copy of some Encyclopedia in his home library. and every town run a local library. So, if for some reason communication with entire world was lost, there were sources of information which can help to solve a problem.

So, we want to build an offline web - an information-exchange network, where each node keeps a local copy
of information which is synchronized with other node each time a possibility arises. 
Sounds much like good old Usenet or FIDO? Yes. These things were invented when communication links were week and no one would rely on immediate availability of a link to other end of world.

But Usenet was invented when computes were big and unmovable. And there were few of them, so each system administrator was able to maintain his own UUCP maps of the world.

Now, if two friends meet in the pub, both probably have something with few gigabytes of storage and high-bandwidth Wi-Fi interface in the pocket. So, while people exchange tidings by the world of mouth, their smartphones or tablets can exchange much more information using ad-hock wi-fi network.

So, there are millions of computers which can be potentially members of this network, and no one could account for all of them. So we should be prepared to synchronize our news spools with a stranger.

One consequence of this is that messages are passed through number of untrusted nodes. So, each message
is protected by digital signature to ensure that in was not changed in the way. 

Of course, if internet is available, we would use it for syncronization. It is also planned to utilize torrent-like protocol to speed-up synchronization if more than two nodes can see each other.

Basic principles of CheshireNet
--------------------------------

1. Every body has full control of the node one owns. This makes it differnet for example from FreeNet. 
  Every node is allowed to filter all information it recieves and keep only what he wants to keep.
2. Each message is proteced by digital signature to prevent tampering.
3. Each signature key represents itself only. We would use some algorithmic way to derive memorizable  nicknames and/or userpics from the key fingerprint. 

