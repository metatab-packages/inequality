# Inequality Collection


## References

The Debt, randal

* [How Does Intergenerational Wealth Transmission Affect Wealth Concentration? ](https://www.federalreserve.gov/econres/notes/feds-notes/how-does-intergenerational-wealth-transmission-affect-wealth-concentration-20180601.htm)
* [The Dynamics of the Racial Wealth Gap](http://www.people.virginia.edu/~ey2d/aliprantis_carroll_young_2019b.pdf)

Feiveson and Sabelhaus calculate that 26% of welath is due to transfers, because they assume that all of the transfer is invested at 3%. This is clearly nonsense.

From [Disparities in Wealth by Race and Ethnicity in the 2019 Survey of Consumer Finances](https://www.federalreserve.gov/econres/notes/feds-notes/disparities-in-wealth-by-race-and-ethnicity-in-the-2019-survey-of-consumer-finances-20200928.htm): 

    By some estimates bequests and transfers account for at least half of aggregate wealth (Gale and Scholz 1994), have recently averaged 3 percent of total household disposable personal income (Feiveson and Sabelhaus 2018), and account for more of the racial wealth gap than any other demographic or socioeconomic indicator (Hamilton and Darrity 2010).8 

 William Gale and John Karl Scholz. 1994. "Intergenerational Transfers and the Accumulation of Wealth." Journal of Economic Perspectives, 8(4): 145-160. Laura Feiveson and John Sabelhaus. 2018. "How Does Intergenerational Wealth Transmission Affect Wealth Concentration?" FEDS Notes. Washington: Board of Governors of the Federal Reserve System, June 1, 2018. Darrick Hamilton and William Darity. 2010. "Can 'Baby Bonds' Eliminate the Racial Wealth Gap in Putative Post-Racial America?" The Review of Black Political Economy 37(3–4): 207–16. Return to text

The Hamiton & Darity reference: 

    Careful economic studies actually demonstrate that inheritances, bequests and intra-family transfers account for more of the racial wealth gap than any other demographic and socioeconomic indicators including education, income and household structure (see for example, Blau and Graham 1990; Menchik and Jianakoplos 1997; Gittleman and Wolff 2004). These intra-familial transfers, the primary source of wealth for most Americans with positive net worth, are transfers of blatant non-merit resources. Why do blacks have vastly less resources to transferto the next generation?
    
Menchik P, Jianakoplos NA. Black-White wealth inequality: is inheritance the reason? Econ Inq. 1997;35(2):428–42:

    Controlling for other factors which contribute to racial differences in wealth, we estimate that financial inheritances may account for between 10% and 20% of the average difference in black‐white household wealth.

Blau and Graham 1990: 

    
[Racial and Ethnic Differences in Wealth and Asset Choices](https://www.ssa.gov/policy/docs/ssb/v64n4/v64n4p1.html)

### Savings

From [Racial and Ethnic Differences in Wealth and Asset Choices](https://www.ssa.gov/policy/docs/ssb/v64n4/v64n4p1.html)

    Hurst, Luoh, and Stafford (1998), using the 1984-1994 Panel Study of Income Dynamics, reported that a large part of the racial difference in wealth accumulation can be attributed to differences in permanent income and portfolio composition. In an examination of wealth accumulation patterns in the first two waves of the Health and Retirement Study (HRS), Smith (1995b) found that minority groups have lower rates of asset accumulation, even after controlling for income, health, bequest motive, and so on.

### Inheritance

A [Fed paper](https://www.federalreserve.gov/econres/notes/feds-notes/how-does-intergenerational-wealth-transmission-affect-wealth-concentration-20180601.htm) finds that inheritances account for a large portion of net worth. 

    In aggregate, the SCF data confirms the findings from the older literature about the direct contribution of intergenerational wealth transfers to wealth accumulation.11 As shown in the last column of Table 2, if we assume that the inflation-adjusted return on transfers received is 3 percent, we estimate that 26 percent of total wealth can be accounted for by intergenerational transfers. Using a real interest rate of 5 percent, the estimated share of wealth accounted for by intergenerational transfers jumps to 51 percent.


## Other Datasets

[Health and Retirement Study](https://hrsdata.isr.umich.edu/data-products/2018-hrs-core)



## Managing the Collection


### Adding an Existing Data Package

Collections are composed of this top level directory and source packages that
are included a git submodules. So, to add a few packages:

  
    git submodule add https://github.com/metatab-packages/sandiegocounty.gov-covid19.git
    git submodule add https://github.com/metatab-packages/census.gov-boundaries-2018.git
    
Then, when checking out the collection, be sure to update all of the submodules too: 

    git clone --recurse-submodules <collection_url>
    
### Adding new data packages. 
    
To add a new package, cd to the staging directory, create the package, then check it in to github. Then use the instructions above to add it to the main directory as a submodule. 

    cd staging
    mp new -o exmaple.com -d datapackage
    cd exmaple.com-datapackage
    < Edit metadata; At least set description and title>
    mp github init
    cd ../
    git submodule add https://github.com/metatab-packages/exmaple.com-datapackage.git
    
The `mp github init` call will set up a new repo on Github for the package. It requires getting an pplication token from Github and adding it to the metatab configuration file. See ``mp github init``
    
    
### Building  packages. 

The top lvel directory defines `invoke` tasks. To use invoke you will need to `pip install invoke`. Then run `invoke -l` to like the available tasks. THe most important are: 

* `invoke build`: Run `mp build` in each package
* `invoke make`: Run `mp make` in each package, which will build the package, upload it to s3 and publish it to Wordpress, with the proper configuration. 