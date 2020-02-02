## Instance Learning

Just simply store training data.

The generalization job delay to classify the new instance.

Sometimes, this method is called `lazy method`.

#### Advantages

- This method doesn't approach the `target function` in the whole instance space by once.
- It just gets the local and different estimation for every new instance.
- We can use less complex `local target function` to approach when the `target function` is so complex.

> So this method can get different `target function` to approach for every new instance.

#### Disadvantages

- May spend a lot when predicting.
    - So how does we index these traning data effectively is important.
- When we index the similar training data, we usually consider all of the attributes, but the truely similar instance may be far away when we only consider part of the attributes


## Algorithms

- KNN
- locally weighted regression



