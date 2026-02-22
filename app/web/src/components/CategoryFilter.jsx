import "./CategoryFilter.css";

export default function CategoryFilter({ categories, selected, onChange, enterpriseCategories = [] }) {
  return (
    <div className="cat-filter" role="tablist" aria-label="Filter by category">
      <button
        type="button"
        role="tab"
        aria-selected={selected === "all"}
        className={`cat-filter-chip ${selected === "all" ? "active" : ""}`}
        onClick={() => onChange("all")}
      >
        All
      </button>
      {categories.map((cat) => {
        const isEnterprise = enterpriseCategories.includes(cat);
        return (
          <button
            key={cat}
            type="button"
            role="tab"
            aria-selected={selected === cat}
            className={`cat-filter-chip ${selected === cat ? "active" : ""} ${isEnterprise ? "enterprise" : ""}`}
            onClick={() => onChange(cat)}
          >
            {cat}
          </button>
        );
      })}
    </div>
  );
}
