mip -- **M**\ CNP **I**\ input file **P**\ arser
====================================================

.. comment:: 

    See mcnp_input_file_parser.rst in notes.


An MCNP input file parser is required in several projects: numjuggler, cR2S.
Current implementation in numjuggler is limited and hardly can be extended to
use it for preparing data for CAD conversion. This package should replace input
file reader in numjuggler and cR2S, and provide additional functionality
necessary for later conversion to CAD.

The parser analyses an input file in steps, each getting deeper information.
Each step can be called independently by the user, but it is the user's
responsibility to provide input information to each step. Each step is
implemented in a separate module.

Steps are:

    * split input to blocks

    * split blocks to cards and inter-card comments

    * split cards to meaningful input and intra-card comments (referred later
      as comments), and extracting format of the card

    * Analysis of cards, necessary for particular needs (e.g. for renumbering
      in numjuggler) should be done separately.


    
