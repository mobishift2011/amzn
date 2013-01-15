<html>
    <head>
    </head>
    <body>
        <table border="1" bordercolor="#000000" cellspacing="0" style="border-collapse:collapse">
            <thead>
                <tr>
                    <th>Task</th>
                    <th>Status</th>
                    <th>Started At</th>
                    <th>Updated At</th>
                    <th>Ended At</th>
                    <th>Dones</th>
                    <th>Updates</th>
                    <th>News</th>
                    <th>Fails</th>
                </tr>
            </thead>
            <tbody>
                % for task in tasks:
                <tr>
                    <td>{{task['name']}}</td>
                    <td>{{task['status']}}</td>
                    <td>{{task['started_at']}}</td>
                    <td>{{task['updated_at']}}</td>
                    <td>{{task['ended_at']}}</td>
                    <td align="right">{{task['dones']}}</td>
                    <td align="right">{{task['updates']}}</td>
                    <td align="right">{{task['news']}}</td>
                    <td align="right">{{task['fails']}}</td>
                </tr>
                % end
            </tbody>
        </table>
    </body>
</html>
