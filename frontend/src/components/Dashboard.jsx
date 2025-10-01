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

    return (
        <div className="space-y-6">
            {/* Most Popular Author */}
            <StatCard title="Most Popular Author" icon="👑">
                <div className="text-center">               
                    <h4 className="font-bold text-gray-900 text-lg mb-1">
                        {data.most_popular_author?.name || "No data available"}
                    </h4>
                    {data.most_popular_author?.bio && (
                        <p className="text-sm text-gray-500 mb-2 line-clamp-2">
                            {data.most_popular_author.bio}
                        </p>
                    )}
                    <div className="flex justify-center gap-4 text-sm">
                        <span className="text-gray-600">
                            👥 {data.most_popular_author?.total_readers?.toLocaleString() || 0}
                        </span>
                        <span className="text-gray-600">
                            📚 {data.most_popular_author?.books_count || 0}
                        </span>
                    </div>
                </div>
            </StatCard>

            {/* User Reading Stats */}
            <StatCard title="Your Reading Stats" icon="📖">
                <div className="space-y-3">
                    <div className="flex justify-between">
                        <span>Books Read:</span>
                        <span className="font-semibold text-green-600">{data.user_books_read?.length || 0}</span>
                    </div>
                    <div className="flex justify-between">
                        <span>Reading Streak:</span>
                        <span>15 days</span>
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
                            <span className="font-medium">{index + 1}. {author.name} ({author.books_count || 0})</span>
                        </div>
                    )) || <p className="text-gray-500">No authors found</p>}
                </div>
            </StatCard>
        </div>
    );
};

export default Dashboard;
