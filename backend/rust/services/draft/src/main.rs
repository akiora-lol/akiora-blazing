mod state;
mod turns;
use bitvec::prelude::*;
fn main() {
    let mut bv: BitArray<[u8; 19], Lsb0> = bitarr!(u8,Lsb0;0;150);
    let mut ar: [u8; 150] = [0; 150];
    bv.set(1, true);
    bv.set(20, true);
    dbg!(bv);

    dbg!(bv[0]);

    dbg!(bv[15]);
    dbg!(bv[20]);
    println!("Size of my_float: {} bytes", size_of_val(&bv));
    println!("Size of my_float: {} bytes", size_of_val(&ar));
}
