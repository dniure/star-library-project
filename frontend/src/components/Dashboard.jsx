/**
 * Dashboard.jsx
 * ----------------
 * Displays dashboard stats for the user:
 * - Most popular author
 * - User reading stats
 * - Top 3 authors
 */

import { StatCard } from "./UIComponents";

const Dashboard = ({ data }) => {
    if (!data) return null;
    
    console.log("top authors: ", data.user_top_authors)

    return (
        <div className="space-y-6">
            {/* Most Popular Author */}
            <StatCard title="Most Popular Author" icon="👑">
                <div className="text-center">
                    <div className="text-4xl mb-2">📚</div>
                    <h4 className="font-bold text-gray-900 text-lg">{(data.most_popular_author?.name || "Unknown")}</h4>
                    <p className="text-gray-600">{data.most_popular_author?.total_readers || 0} readers</p>
                    <p className="text-sm text-gray-500 mt-1">{data.most_popular_author?.books_count || 0} books</p>
                </div>
            </StatCard>

            {/* User Reading Stats */}
            <StatCard title="Your Reading Stats" icon="📖">
                <div className="space-y-3">
                    <div className="flex justify-between">
                        <span>Books Read:</span>
                        <span className="font-semibold text-green-600">{data.books_read?.length || 0}</span>
                    </div>
                    <div className="flex justify-between">
                        <span>Avg Rating:</span>
                        <span className="font-semibold">⭐⭐⭐⭐☆</span>
                    </div>
                </div>
            </StatCard>

            {/* Top 3 Authors */}
            <StatCard title="Your Top 3 Authors" icon="🏆">
                <div className="space-y-2">
                    {data.user_top_authors?.map((author, index) => (
                        <div key={author.id} className="flex justify-between items-center">
                            <span className="font-medium">{index + 1}. {author.name}</span>
                            <span className="text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded">{author.books_count || 0} books</span>
                        </div>
                    )) || <p className="text-gray-500">No authors found</p>}
                </div>
            </StatCard>
        </div>
    );
};

export default Dashboard;
