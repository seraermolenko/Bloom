import { useEffect, useState } from 'react';
import { Bar, BarChart, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { PlantInGarden } from '../types/models';

export type StatusHistoryItem = {
  date_changed: string;
  status: 'Thirsty' | 'Happy' | 'Wet' | null;
};

type Props = {
  personalPlant: PlantInGarden;
  onClose: () => void;
};

export default function StatusChartModal({ personalPlant, onClose }: Props) {
  const [statusHistory, setStatusHistory] = useState<StatusHistoryItem[]>([]);
  const [weekOffset, setWeekOffset] = useState(0);

  useEffect(() => {
    const fetchStatusHistory = async () => {
      try {
        const response = await fetch(`/get_status_history/?plant_id=${personalPlant.personal_plant_id}`);
        const data = await response.json();
        setStatusHistory(data.status_history || []);
      } catch (error) {
        console.error('Error fetching status history:', error);
      }
    };

    fetchStatusHistory();
  }, [personalPlant]);

  function getLast7Days(offset = 0): string[] {
    const days: string[] = [];
    const now = new Date();
    for (let i = 6; i >= 0; i--) {
      const d = new Date(now);
      d.setDate(d.getDate() - i - offset * 7);
      days.push(d.toLocaleDateString());
    }
    return days;
  }

  const activeDates = getLast7Days(weekOffset);

  const chartData = activeDates.map((date) => {
    const matchingItems = statusHistory.filter(
      (item) => new Date(item.date_changed).toLocaleDateString() === date
    );
    const counts = { date, Thirsty: 0, Happy: 0, Wet: 0 };
    for (const item of matchingItems) {
      if (item.status !== null) {
        counts[item.status] += 1;
      }
    }
    const total = counts.Thirsty + counts.Happy + counts.Wet || 1;
    return {
        date,
        Thirsty: counts.Thirsty / total,
        Happy: counts.Happy / total,
        Wet: counts.Wet / total,
        raw: counts 
      };
  });

  const chartConfig = {
    Thirsty: {
      label: 'Thirsty',
      color: 'var(--earth)',
    },
    Happy: {
      label: 'Happy',
      color: 'var(--clay-blush-dark)',
    },
    Wet: {
      label: 'Wet',
      color: 'var(--water)',
    },
  };

  return (
    <div className="modal-overlay wide-modal">
      <div className="modal wide-modal" style={{
            position: 'fixed',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            zIndex: 1000, 
            background: 'white',
            borderRadius: '10px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
            padding: '20px',
        }}>
        <h2>Status History for {personalPlant.custom_name || personalPlant.common_name}</h2>
        <Card>
          <CardHeader>
            <CardTitle>Showing: {activeDates[0]} → {activeDates[6]}</CardTitle>
          </CardHeader>
          <CardContent>
          <div className="chart-wrapper" style={{ width: '100%' }}>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={chartData} margin={{ top: 0, right: 0, left: 0, bottom: 10 }} barCategoryGap={10}>
                    <XAxis dataKey="date" tickLine={false} axisLine={false} tickMargin={10} />
                    <YAxis hide domain={[0, 1]} />
                    <Bar dataKey="Wet" stackId="a" fill={chartConfig.Wet.color} radius={[0, 0, 0, 0]} />
                    <Bar dataKey="Happy" stackId="a" fill={chartConfig.Happy.color} radius={[0, 0, 0, 0]} />
                    <Bar dataKey="Thirsty" stackId="a" fill={chartConfig.Thirsty.color} radius={[4, 4, 0, 0]} />
                    <Tooltip formatter={(_, name, props) => {const raw = props.payload?.raw; return `${name} : ${raw?.[name] || 0}`;}}cursor={false} />
                  </BarChart>
                </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '10px', marginTop: '10px' }}>
          <button onClick={() => setWeekOffset(prev => prev + 1)}>Previous Week</button>
          <button disabled={weekOffset === 0} onClick={() => setWeekOffset(prev => prev - 1)}>Next Week</button>
        </div>
        <div className="modal-actions">
          <button onClick={onClose} className="cancel-button">Close</button>
        </div>
      </div>
    </div>
  );
}
