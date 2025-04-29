drop function transition_median cascade;

create or replace function transition_median(state float8[], value int)
returns float8[]
language plpython3u
as $$
state.append(value)

return state
$$;

create or replace function finalize_median(state float8[])
returns float8
language plpython3u
as $$
if len(state) == 0:
    return None

state.sort()

n = len(state)
if n % 2 == 1:
    return state[n // 2]
else:
    return (state[n // 2 - 1] + state[n // 2]) / 2
$$;

create or replace aggregate median(int) (
    sfunc = transition_median,
    stype = float8[],
    initcond = '{}',
    finalfunc = finalize_median
);

select median(age) from animals;