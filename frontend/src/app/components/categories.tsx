'use client'

import { useState } from 'react';

export const categorieslist = [
    {
        id: 1,
        categoryname: "Mobile Phones",
        logo: "/images/iitpkdlogo.jpg"
    },
    {
        id: 2,
        categoryname: "Properties",
        logo: "/images/iitpkdlogo.jpg"
    },
    {
        id: 3,
        categoryname: "Vehicles",
        logo: "/images/iitpkdlogo.jpg"
    },
    {
        id: 4,
        categoryname: "Bikes",
        logo: "/images/iitpkdlogo.jpg"
    },
    {
        id: 5,
        categoryname: "Bussiness/Industrial",
        logo: "/images/iitpkdlogo.jpg"
    },
    {
        id: 6,
        categoryname: "Houses",
        logo: "/images/iitpkdlogo.jpg"
    },
]


function Category({ categoryname, logo }: { categoryname: string, logo: string }) {
    return (
        <><div>
            <img className="w-20 h-20 rounded-full" alt={categoryname} src={logo}></img>
            <div className=" text-wrap">
                <p className="max-w-20 break-words text-wrap">{categoryname}</p>
            </div></div>
        </>)
}

export default function BrowseCategory() {
    const [showmore, setShowmore] = useState(0);
    let categories = categorieslist.map(category => <Category key={category.id} categoryname={category.categoryname} logo={category.logo}></Category>)
    if (showmore == 0) {
        categories = categories.slice(0, Math.min(categories.length, 4));
    }   
    return (
        <>
            <div>
                <div className='justify-between w-1/2 flex'>
                    <div className='font-semibold text-lg'>Browse Category</div>
                    <div onClick={() => {
                        if (showmore == 0) {
                            setShowmore(1);
                        }
                        else {
                            setShowmore(0);
                        }
                    }}><button className='cursor-pointer hover:text-[#34a8eb]'>Show more....</button></div>
                </div >
                <div className='grid grid-cols-4 w-1/2 border-2 border-black border-solid'>
                    {categories}
                </div>
            </div>
        </>
    )
}