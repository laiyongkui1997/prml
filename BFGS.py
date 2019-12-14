#!/usr/bin/bash python3
#-*- coding: utf8 -*-

"""
algorithm introduction

domain: unconstrained optimization problem
description: the optimization of `Quasi-Newton method`. 
    There are four method to solve unconstrained optimization problem: 
        1. Gradient Descent method, 
        2. Newton method, 
        3. Quasi-Newton method, 
        4. BFGS and L-BFGS.
    
    Goal:
        Find the minimum point of function `f(x)` by updating parameter `x` step by step.
        Result is `x*`

    Gradient descent method:
        Note: All gradient descent related methods will use Taylor's series(泰勒级数) which says 
              a function `f(x)` has `n+1` order derivative in the neighborhood of point `x0`.
              So function `f(x)` can unfold as a `n` order Taylor's series in that neighborhood as shown in follow:
                    ` f(x) = f(x0) + ∇f(x0)(x-x0) + ( ∇f(x0)(x-x0) )^2 / 2! + ... + ( ∇f(x0)(x-x0) )^n / n! `
        
        Content: Use first order Taylor's series to deduce(推导) how to update parameter `x`.
                    ` f(x) = f(x𝑘) + ∇f(x𝑘)(x-x𝑘) ` => ` f(x𝑘) - f(x) = - ∇f(x𝑘)(x-x𝑘) `
                 
                 The goal is to minimize `f(x)`, the same as maximize `f(x𝑘) - f(x)`,
                 the same as minimize `∇f(x𝑘)(x-x𝑘)`.
                 
                 Because `∇f(x𝑘)` is a constant for `x`, so when `x - x𝑘 = - ∇f(x𝑘)`, `∇f(x𝑘)(x-x𝑘)` will be minimum.
                 
                 Then we can get the updating formula of parameter `x`: `x_{k+1} := x𝑘 - ∇f(x𝑘)`.
                 
                 Most of the time, we want to control the step scale(步距) we move, 
                 so we usually add a scale coefficient for `∇f(x𝑘)`, we call it `𝛼`.

                 The result updating formula of parameter `x` is `x_{k+1} := x𝑘 - 𝛼∇f(x𝑘)`.
        
    Newton method:
        Note: The properties of positive definite matrices(正定矩阵, PDM): 
                `A` is PDM when there is a matrix X make the formula `X A X > 0` is right.

        Content: Use second order Taylor's series to deduce how to update parameter 'x'.
                    ` f(x) = f(x𝑘) + ∇f(x𝑘)(x-x𝑘) + 1/2 (x-x𝑘)^T ∇f(x𝑘)^2 (x-x𝑘) `
                 
                 The goal is to minimize `f(x)`, the same as when get parameter `x` from `∇f(x) = 0`
                 `f(x)` is the minimum (Because `f(x)` is a second order function).

                 => ` ∇f(x𝑘) +  ∇f(x𝑘)^2 (x-x𝑘) = 0`
                 => ` x_{k+1} := x𝑘 - H^(-1) ∇f(x𝑘) `, in which `H = ∇f(x𝑘)^2`

                 The updating direction of parameter `x` is `- H^(-1) ∇f(x𝑘) ` which goes in opposite direction with `∇f(x𝑘)`,
                 so we can derivate the formula: ` - ∇f(x𝑘) H^(-1) ∇f(x𝑘) < 0`, 
                 which clearly show that the Hesse Matrix (`H^(-1)`) need to be positive definite matrices(正定矩阵).
                 This is the a disadvantage of `Newton method`.

                 As usually, we should control the step scale in updating direction,
                 but it is different from `Gradient descent method`, we should choose the best step scale.
                 => 𝜆k = arg min f( x𝑘 - 𝜆k H^(-1) ∇f(x𝑘) )

                 The result updating formula of parameter `x` is `x_{k+1} := x𝑘 - 𝜆k H^(-1) ∇f(x𝑘)`
                 where `𝜆k = arg min f( x𝑘 - 𝜆k H^(-1) ∇f(x𝑘) )`.

        Conclusion: 1. Need calculate Hesse Matrix which cost a lot computation, 
                       and limit Hesse Matrix to be Positive Definite Matrices.
                    2. Newton method is second order convergence(收敛), 
                       if the second order derivation `Δ(𝑥𝑘)` is not positive (0 or negetive),
                       then the direction of `x_{k+1}` may not be the right descent direction.
                    3. Newton method uses a quadric(二次曲面) to fit the local surface of current point,
                       while Gradient descent method use a plane(平面) to fit,
                       which make Newton method more suitable for the real optimal descent path(最优下降路径).

    Quasi-Newton method:
        Content: It overcomes the biggest disadvantage for large computation. 
                 It uses a Symetric Positive Definite Matrix(对称正定矩阵) of approximate Hesse Matrix 
                 rather than calculate the Hesse Matrix of objective function.

                 As same as Newton method, we unfold `f(x)` in `x_{k+1}`:
                    ` f(x) = f(x_{k+1}) + ∇f(x_{k+1})(x-x_{k+1}) + 1/2 (x-x_{k+1})^T ∇f(x_{k+1})^2 (x-x_{k+1}) `
                
                 Then we derivate `x_{k+1}` in both sides: 
                    => ` ∇f(x) = ∇f(x_{k+1}) + ∇f(x_{k+1})^2 (x-x_{k+1}) `
                    => ` ∇f(x) = ∇f(x_{k+1}) + H_{k+1} (x-x_{k+1}) `, `H_{k+1} = ∇f(x_{k+1})^2`
                
                 Make `x = x𝑘`, => ` ∇f(x𝑘) = ∇f(x_{k+1}) + H_{k+1} (x𝑘-x_{k+1}) `
                    => ` ∇f(x_{k+1}) - ∇f(x𝑘) =  H_{k+1} (x_{k+1} - x𝑘) `

                 There, we can use a Symetric Positive Definite Matrix `B_{k+1}` to replace Hesse Matrix `H_{k+1}` as follow:
                    => ` ∇f(x_{k+1}) - ∇f(x𝑘) =  B_{k+1} (x_{k+1} - x𝑘) `
                 which is `Quasi-Newton Conditions`.

                 Then the problem is how to construct this Symetric Positive Definite Matrix(对称正定矩阵),
                 there are two methods:
                    1. BFGS
                    2. L-BFGS

        BFGS:
            Content: 1. Initialize B0 = I
                     2. Updating `B_{k+1} = B𝑘 + ΔB𝑘, k=1, 2, ...` iteratively

                     How to caculate ΔB𝑘?
                        => ` ΔB𝑘 = 𝛼𝑢𝑢^𝑇+𝛽𝑣𝑣^𝑇 `, `𝑢` and `𝑣` is unkonwn.
                     which make sure that `ΔB𝑘` is a Symetric Positive Definite Matrix(对称正定矩阵).

                     According `Quasi-Newton Conditions`:
                        => ` ∇f(x_{k+1}) - ∇f(x𝑘) =  B_{k+1} (x_{k+1} - x𝑘) `
                                                 = ` (B𝑘 + ΔB𝑘)(x_{k+1} - x𝑘) `
                                                 = ` (B𝑘 + 𝛼𝑢𝑢^𝑇+𝛽𝑣𝑣^𝑇)(x_{k+1} - x𝑘) `
                                                 = ` B𝑘·(x_{k+1} - x𝑘) + ( 𝛼𝑢^𝑇·(x_{k+1} - x𝑘) )·𝑢 + ( 𝛽𝑣^𝑇·(x_{k+1} - x𝑘) )·𝑣 `
                        To simplity the formula, we define 
                            `Δx𝑘 = (x_{k+1} - x𝑘)` and 
                            `Δf𝑘 = ∇f(x_{k+1}) - ∇f(x𝑘)`, 
                        then the above formula can be present as follow:
                            => ` Δf𝑘 =  B𝑘·Δx𝑘 + ( 𝛼𝑢^𝑇·Δx𝑘 )·𝑢 + ( 𝛽𝑣^𝑇·Δx𝑘 )·𝑣 `
                        where `𝛼𝑢^𝑇·Δx𝑘` and `𝛽𝑣^𝑇·Δx𝑘` is real.
                    
                    So we can make equation as follow:
                        => `𝛼𝑢^𝑇·Δx𝑘 = 1`
                        => `𝛽𝑣^𝑇·Δx𝑘 = -1`
                    Then `𝑢 - 𝑣 = Δf𝑘 - B𝑘·Δx𝑘`,
                    where we can get a approximate result:
                        => `𝑢 = Δf𝑘`
                        => `𝑣 = B𝑘·Δx𝑘`
                    
                    ----- (Get the result `𝑢` and `𝑢`) -----

                        => `𝛼 = 1 / (𝑢^𝑇·Δx𝑘) = 1 / ( (Δf𝑘)^𝑇 · Δx𝑘 )`
                        => `𝛽 = -1 / (𝑣^𝑇·Δx𝑘) = 1 / ( (B𝑘·Δx𝑘)^𝑇 · Δx𝑘 ) = 1 / ( (Δx𝑘)^𝑇 · B𝑘 · Δx𝑘 )`
                            where `B𝑘` is a Symetric Positive Definite Matrix(对称正定矩阵)

                    ----- (Get the result `𝛼` and `𝛼`) -----

                        => `ΔB𝑘 = 𝛼𝑢𝑢^𝑇 + 𝛽𝑣𝑣^𝑇 `
                                = ` (Δf𝑘 · (Δf𝑘)^T ) / ( (Δf𝑘)^𝑇 · Δx𝑘 ) `
                                    + ` (B𝑘 · Δx𝑘 · (Δx𝑘)^T · B𝑘) / ( (Δx𝑘)^𝑇 · B𝑘 · Δx𝑘 )`
                    
                    ----- (Get the result `ΔB𝑘`) -----

            Problem: The direction of Newton method is `- H𝑘^(-1) ∇f(x𝑘)`, so we should caculate `B𝑘^(-1)`.
                     The best solution is caculating `B𝑘^(-1)` directly rather than caculating `B𝑘`.

    for more information, please see: 
        http://note.youdao.com/noteshare?id=2483fa0c28f55d3ea00e538fd4549e70

"""

import os
import numpy as np
import matplotlib.pyplot as plt


def draw_result(x, y):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set(xlabel='x', ylabel='y', title='test function')
    ax.grid()
    plt.show()


def BFGS(fn, delta_fn, stop_fn=None, x_0=0, max_steps=50):
    results = []
    I = np.eye(x_0.shape[0])
    D = I
    b = 0.55
    p = 0.4
    sigma = 0.6
    for _ in range(max_steps):
        d = - np.dot(D, delta_fn(x_0))  # direction = - H * f'
        m = 0
        while m < 20:
            a = b**m
            # half Armijo condition (in this test, can reach the optimal point)
            # if fn(x_0 + a * d) <= fn(x_0) + p*a*np.dot(np.mat(delta_fn(x_0)).T, d):

            # full Armijo condition (in this test, can not reach the optimal point)
            # if fn(x_0 + a * d) <= fn(x_0) + p*a*np.dot(np.mat(delta_fn(x_0)).T, d) and \
            #     fn(x_0 + a * d) >= fn(x_0) + (1-p)*a*np.dot(np.mat(delta_fn(x_0)).T, d):

            # full Wolfe condition (in this test, can reach the optimal point)
            if fn(x_0 + a * d) <= fn(x_0) + p*a*np.dot(np.mat(delta_fn(x_0)).T, d) and \
                np.dot(np.mat(delta_fn(x_0 + a * d)).T, d) >= sigma * np.dot(np.mat(delta_fn(x_0)).T, d):
                break
            m += 1
        
        d_x = b**m * d
        prev_x_0 = x_0
        x_0 += d_x
        d_f = np.matrix(delta_fn(x_0) - delta_fn(prev_x_0))
        if np.dot(d_x.T, d_f) != 0:
            D = D + (1.0 / np.dot(d_x.T, d_f) + np.dot(np.dot(d_f.T, D), d_f) / np.dot(d_x.T, d_f)**2 ) * np.dot(d_x, d_x.T)
            D = D - 1.0 / np.dot(d_x.T, d_f) * ( np.dot(np.dot(D, d_f), d_x.T) + np.dot(np.dot(d_x, d_f.T), D) )
        results.append((x_0, fn(x_0)))
    return results

if __name__ == '__main__':
    """running mode"""
    ''' test function '''
    #function
    def fn(x):
        return 100 * (x[0,0] ** 2 - x[1,0]) ** 2 + (x[0,0] - 1) ** 2
    
    #dleta function
    def delta_fn(x):
        result = np.zeros((2, 1))
        result[0, 0] = 400 * x[0,0] * (x[0,0] ** 2 - x[1,0]) + 2 * (x[0,0] - 1)
        result[1, 0] = -200 * (x[0,0] ** 2 - x[1,0])
        return result
    
    ''' test BFGS '''
    x0 = np.mat([[-1.2], [1]])
    results = BFGS(fn, delta_fn, x_0=x0)
    plot_x = np.arange(0, len(results), 1)
    plot_y = [item[1] for item in results]
    draw_result(plot_x, plot_y)

