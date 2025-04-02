import { createFetch } from "next/dist/client/components/router-reducer/fetch-server-response"
import BrowseCategory from "./components/categories"
import { categorieslist } from "./components/categories"
export default function App() {
    let categories = categorieslist.map(category => <BrowseCategory categoryname={category.categoryname} logo={category.logo}></BrowseCategory>)
    return (
        <>
            {categories}
        </>
    )
}