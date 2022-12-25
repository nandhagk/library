# Lets think about the multithreadings
# I need to have only one thread for layouting (to avoid race conditions)
# Rendering will be done on the main thread
# for event handling we can spawn multiple threads? (i.e use a qthreadpool)
# and even for event callbacks we can spawn multiple threads (i.e use a qthreadpool for callbacks)
# And then the emitter will wait for this worker to finish then propogate upwards
# Yes
# Think about race conditions after finishing this shit
# Worst case we can limit the initial threadpool to just 1
