#Kaldi help for this file:
# you can change cmd.sh depending on what type of queue you are using.
# If you have no queueing system and want to run on a local machine, you
# can change all instances 'queue.pl' to run.pl (but be careful and run
# commands one by one: most recipes will exhaust the memory on your
# machine).  queue.pl works with GridEngine (qsub).  slurm.pl works
# with slurm.  Different queues are configured differently, with different
# queue names and different ways of specifying things like memory;
# to account for these differences you can create and edit the file
# conf/queue.conf to match your queue's configuration.  Search for
# conf/queue.conf in http://kaldi-asr.org/doc/queue.html for more information,
# or search for the string 'default_config' in utils/queue.pl or utils/slurm.pl.

#Peter Smit's cmd.sh, commented out:
#export mfcc_cmd="slurm.pl --mem 2G"
#export base_cmd="run.pl"
#export train_cmd="run.pl"
#export decode_cmd="run.pl"
#export big_decode_cmd="run.pl"
#export mkgraph_cmd="run.pl"
## the use of cuda_cmd is deprecated.
#export cuda_cmd="run.pl --gpu 1"
#export par_cmd="slurm.pl --mem 2G"
#I think Peter used run.pl so often because he would build his own recipes, 
# and use his job command from his common/slurm_dep_graph.sh

#This is Aku's cmd.sh, which should work for the Kaldi style recipes.
#Specifically, like you see in http://kaldi-asr.org/doc/queue.html,
# the slurm.pl script supports some general options,
# most importantly --gpu 1 (provided you have it setup correctly in conf/slurm.conf for our cluster)
# this way everything can just call slurm.pl and the script will request gpu nodes only when necessary.
export mfcc_cmd="slurm.pl"
export base_cmd="slurm.pl --mem 2G --time 2:00:00"
export train_cmd="slurm.pl --mem 2G --time 2:00:00"
export decode_cmd="slurm.pl --mem 2G --time 2:00:00"
export big_decode_cmd="slurm.pl"
export mkgraph_cmd="slurm.pl"
# the use of cuda_cmd is deprecated.
export cuda_cmd="slurm.pl --gpu 1"
export par_cmd="slurm.pl"
export emb_cmd="slurm.pl --gpu 1"

